// Convert next-mdx-remote compiledSource to HTML WITHOUT executing it:
// parse to an AST with acorn and interpret only the tiny subset it uses
// (_jsx/_jsxs calls, object/array literals, strings, _components.x lookups).
import fs from 'fs';
import * as acorn from 'acorn';
const [,, inFile, outFile] = process.argv;
const data = JSON.parse(fs.readFileSync(inFile, 'utf8'));
const VOID = new Set(['img','br','hr','input']);
const esc = s => String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
const attr = s => String(s).replace(/&/g,'&amp;').replace(/"/g,'&quot;');

function render(n) {
  if (n == null || n === false || n === true) return '';
  if (Array.isArray(n)) return n.map(render).join('');
  if (typeof n === 'string' || typeof n === 'number') return esc(n);
  if (n.__el) {
    const { children, ...rest } = n.props;
    const a = Object.entries(rest).filter(([k,v]) => v != null && v !== false && k !== 'style')
      .map(([k,v]) => ` ${k === 'className' ? 'class' : k}="${attr(v)}"`).join('');
    if (n.type === 'Fragment') return render(children);
    if (VOID.has(n.type)) return `<${n.type}${a}>`;
    return `<${n.type}${a}>${render(children)}</${n.type}>`;
  }
  return '';
}

function evalNode(node, comps) {
  switch (node.type) {
    case 'Literal': return node.value;
    case 'TemplateLiteral': return node.quasis.map(q => q.value.cooked).join('');
    case 'ArrayExpression': return node.elements.map(e => evalNode(e, comps));
    case 'ObjectExpression': {
      const o = {};
      for (const p of node.properties) {
        const k = p.key.type === 'Identifier' ? p.key.name : p.key.value;
        o[k] = evalNode(p.value, comps);
      }
      return o;
    }
    case 'MemberExpression': {
      if (node.object.name === '_components') return comps[node.property.name] ?? node.property.name;
      throw new Error('unsupported member');
    }
    case 'Identifier':
      if (node.name === '_Fragment') return 'Fragment';
      if (node.name === 'undefined') return undefined;
      throw new Error('unsupported identifier ' + node.name);
    case 'CallExpression': {
      const f = node.callee.name;
      if (f === '_jsx' || f === '_jsxs') {
        const type = evalNode(node.arguments[0], comps);
        const props = node.arguments[1] ? evalNode(node.arguments[1], comps) : {};
        if (typeof type !== 'string') throw new Error('component not a tag');
        return { __el: true, type, props };
      }
      throw new Error('unsupported call ' + f);
    }
    case 'UnaryExpression':
      if (node.operator === '-') return -evalNode(node.argument, comps);
      throw new Error('unsupported unary');
    default: throw new Error('unsupported node ' + node.type);
  }
}

function convert(src) {
  const ast = acorn.parse(src, { ecmaVersion: 2022, allowReturnOutsideFunction: true });
  // collect the _components default map: Object.assign({ p: "p", ... }, ...)
  const comps = {};
  let root = null;
  (function walk(n) {
    if (!n || typeof n !== 'object') return;
    if (n.type === 'CallExpression' && n.callee.type === 'MemberExpression' &&
        n.callee.object.name === 'Object' && n.callee.property.name === 'assign' &&
        n.arguments[0]?.type === 'ObjectExpression') {
      for (const p of n.arguments[0].properties) comps[p.key.name || p.key.value] = p.value.value;
    }
    if (n.type === 'ReturnStatement' && n.argument && n.argument.type === 'CallExpression' && !root &&
        ['_jsx','_jsxs'].includes(n.argument.callee.name)) root = n.argument;
    for (const k of Object.keys(n)) {
      const v = n[k];
      if (Array.isArray(v)) v.forEach(walk); else if (v && typeof v.type === 'string') walk(v);
    }
  })(ast);
  if (!root) throw new Error('no root');
  return render(evalNode(root, comps));
}

const out = {};
for (const [key, val] of Object.entries(data)) {
  const src = val && val.source && val.source.compiledSource;
  if (!src) continue;
  try { out[key] = convert(src); } catch (e) { console.error('FAIL', key, e.message); }
}
fs.writeFileSync(outFile, JSON.stringify(out));
console.log(Object.entries(out).map(([k,v]) => k + ' ' + v.length).join('\n'));
