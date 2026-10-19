module Jekyll
  module LanguageFilter
    def where_tag(array, tag)
      array.select { |item| item.tags.include?(tag) }
    end
  end
end
Liquid::Template.register_filter(Jekyll::LanguageFilter)
