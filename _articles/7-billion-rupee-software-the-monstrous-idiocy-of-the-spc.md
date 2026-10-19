---
title: "7-Billion Rupee Software: The Monstrous Idiocy of the SPC"
lang: en
translation_key: "7-billion-rupee-software-the-monstrous-idiocy-of-the-spc"
slug: "7-billion-rupee-software-the-monstrous-idiocy-of-the-spc"
permalink: /article/7-billion-rupee-software-the-monstrous-idiocy-of-the-spc/
date: 2022-06-17
kind: analysis
category: healthcare
categories: [healthcare, special-reports]
contributors: [yudhanjaya-wijeratne, nisal-periyapperuma, aisha-nazim, mohamed-fairooz, nishadi-gunatilake]
description: "What does the State Pharmaceuticals Corporation want, exactly? We read the documentation so you don’t have to. Welcome to one of the stupidest software requests we’ve seen."
image: /images/library/2d3c9a169534.webp
original_url: "https://watchdog.team/article/7-billion-rupee-software-the-monstrous-idiocy-of-the-spc"
credits:
  - {label: "story", names: "Yudhanjaya Wijeratne & Nisal Periyapperuma"}
  - {label: "edited", names: "Aisha Nazim"}
  - {label: "translation", names: "Mohammed Fairooz & Nishadi Gunatilake"}
---

## A little bit of context {#h-a-little-bit-of-context}

The State Pharmaceutical Corporation (SPC) made headlines recently at the Committee On Public Enterprises (COPE) hearing in the Sri Lankan Parliament.

Specifically, when asked about their operations, they claimed that they needed seven billion rupees for software to run their whole enterprise.

This links into some recent drama. The Medical Supplies Division (MSD), which works hand-in-hand with SPC, has existing software that is truly memworthy: Rs. 644 million spent over seven years (2008 – 2015), and not functional. [As Readme.lk noted, this in itself is a ludicrous figure](https://readme.lk/spc-has-paid-lkr-644-million-for-software-that-doesnt-work/) - "just a little under 50 million short of hSenid (a major software company in Sri Lanka)’s IPO offering in December."

SPC clearly has massive inventory management problems: between 2011 and 2020, [Rs. 6,259 million worth of drugs faced a quality failure](https://www.parliament.lk/en/news-en/view/2577) due to improper storage of drugs — by the SPC.

[https://vimeo.com/796542743](https://vimeo.com/796542743)

Now, the 644 million rupee figure is up for debate. It's been contested by e-Wis, the people who were supplying said software. Nevertheless, both sums are ludicrous, especially in the midst of Sri Lanka's economic collapse.

Even Parliamentarians were aghast: MP Dr. Harsha De Silva took a hard line with the questions, calling it ‘criminal’, and COPE Chair Dr. Charith Herath openly called for the tech community in Sri Lanka to help build software that can handle "inventory management, procurement management, and need assessment.”

And it looks like not only can *that* software be built, it can be done for a whole lot cheaper, as we’ve been publicly saying so far. In fact, a rather odd snippet highlighted by Dr. Beshan Kulapala, Director and co-founder of Vega Innovations, is that a tender had already been handed out to a much newer company, Loons Lab, to replace the existing [“Rs 644 million rupee” system for Rs 100 million](https://www.newswire.lk/2022/06/08/it-industry-responds-to-cope/). \[1\]

The 7 billion rupee, however, is interesting. It’s a number suggested by the University of Colombo (not from a software company doing the bid). Our question: What on earth justified this seven billion rupee figure? What exactly did SPC, MSD and/or the Ministry of Health ask for to justify such a huge number?

To understand the specifics of the matter, let's first look at the broad category of software that the SPC wants: an ERP.

## What’s an ERP? {#h-whats-an-erp}

ERPs are complex command-and-control applications for large organizations.

Their origin lies in 1964, when toolmaker Black and Decker adopted a computerized production scheduling system. Over the decades, computers grew to handle various functions of businesses: think finance, inventory control, accounting, supply chain management, HR. By the 1990s, software vendors were stapling all these very different functions to each other and selling the lot as one package.  The general idea was that almost everything a company did could be handled by a single piece of software.

The quintessential ERP is a monolithic beast that lets big businesses oversee and handle their core functions from one place. Today's ERPs are enormously complex, and software vendors themselves are big businesses in their own right.

Many commercial ERP systems are so big and complex that armies of other software corporations (known as system integrators) take on the task of installing and customizing them to fit customer corporations.

*"This is the UNIX philosophy: write programs that do one thing and do it well...the notion of 'beautiful and intricate complexities' is an oxymoron."* - Doug McIlroy, head of Bell Labs Computing Sciences Research Center

In essence, they are the very opposite of McIlroy’s UNIX programs. We say this not to impose a particular philosophy of software design, but to help you understand that an ERP is, by design, a Frankenstein's monster of functionality.

 ![Frankenstein’s monster. WikiMedia Commons.](/images/library/addd3cc72942.webp)

## What does SPC want from *their* ERP? {#h-what-does-spc-want-from-their-erp}

To answer this, we obtained a Request For Proposals (RFP) put out by the State Pharmaceuticals Corporation in 2021. This is the closest match we can find to the seven billion rupee request for a new system. Multiple stakeholders are listed: the SPC, which procures; the Medical Supplies Division (MSD); and pretty much the entire government health infrastructure.

Here’s the source document as a PDF. Copying was locked by the original publisher - we’ve gone ahead and unlocked it.

[IT ERP2021-unlocked.pdf 1804542](https://watchdog-public-assets.sgp1.digitaloceanspaces.com/attachments/4cf29ce9-a2b2-43d5-9417-0012dc9ad856)

We first read all 183 pages of it to understand exactly what the SPC was asking for.

We then used the following methodology:

1. Extracted Annex 03 and other technical specifications and bucket them under the department / subsystem making the request
2. Read every line item under a particular department
3. Assigned red flags. Red flags are things that make us go WTF; they’re blatantly outside Dr. Charith Herath’s request for "*inventory management, procurement management, and need assessment*.” The classification is not perfect - no doubt someone at SPC can argue that tracking uniforms and milk powder are the needs of the day; this is merely us flagging stuff that we believe should be examined twice.
4. Assigned a WTF score for each department. This is based on the number of times we went “what the fuck?” while reading a particular section, divided by the number of line items, then bucketed into one of three bands (LOW, MEDIUM, HIGH).

 ![](/images/library/291bb3a8194f.webp)

The process of digging out these gems.

These per-department requests and scores are available in a publicly commentable spreadsheet linked below.

Our verdict: not only has the SPC wasted hundreds of millions on software already: their new seven billion rupee software, by design, is an impossible request. It is one of the most ludicrously complex spec sheets we've ever seen.

 ![Hercules and the Lernaean Hydra, from Etruria, attributed to the Painter of Aquila, 530-500 BCE. By Carole Raddato, 2014, under Creative Commons Attribution-ShareAlike.](/images/library/7abc379933b4.webp)

Let’s have a look at some of the biggest red flags we noted. Our comments below are in blue.

 1. Milk powder use between departments ‘*When issuing controllable items( Milk powder, Suger) relevant departments should have a facility to identify when limits are exceeded.’* why is this one of the first requests? And why do you need software for this?
 2. Availability of parking space why? this is an incredibly complex problem: you either need a lot of iOT hardware or humans painstakingly updating when cars are parked and where. Parking management systems (like 4Park) are separate software suites in their own right.
 3. Car parking payments why? Are car parking payments a core part of the SPC business model? If so, please rename to State Parking Corporation.
 4. Vehicle and driver availability, linked with an attendance monitoring system this is what Uber/PickMe/Lyft/Grab does
 5. Vehicle fuel, repairs, battery and air conditioner status; in fact, a whole bunch of stuff related to vehicles: \* *Facility to maintain vehicle details (Vehicle No,Type,Date of registration, pool or staff, department... etc) \* Facility to maintain repair & service details (repair type, cost of repair...etc) \* System should facilitate to identify license expiry dates, battery expiry, vehicle air condition expiry, service due dates \* Facility to record running chart summary details (monthly milage)* this is more functionality than Uber has. Either they’re expecting Tesla levels of integration going on or every driver will have a side job as a data entry operator. Why this much effort on this problem?
 6. Repair details of office equipment, including warranty and service details and notifications specialized asset-tracking software companies like Coast, Asset Panda, ProntoForms and eZOfficeInventory exist for this
 7. Tenders. preparing tender invitation letters; but also to record tenders, store minutes of meetings related to tenders, generate print ads for tenders, and publish to web — this pops up a lot across departments. Multiple departments want this facility, but there also is a separate body within the SPC (Procurement Management) that specializes in this; there’s also an entire subsection that details the process. Judging by the mangled tender we’re reading, SPC could use something to help them. However, tenders creation and management software is, in itself, a complicated field with very specialized software offerings. RIB Software, for example, has an e-tendering system [used by a lot of the German government](https://www.rib-software.com/en/solutions/e-business-and-e-tendering): to build software that works that well would be a daunting task. Also, why are you generating ads? Why does this need the functionality of Adobe InDesign / Canva?
 8. “Co-ordinate of all high values construction works. Planning of Layouts and designing of internal structures for new Osu Sala’s and other departments.” (and, in the same spec): “Handle with Janitorial service – Co-ordination of all tasks carried out by Janitors.” fortunately, the spec stops short of demanding full-blown CAD (Computer Aided Design) software; however, they do want this software to handle the financials and reporting on all construction work carried out by SPC. Why?
 9. Facility to record advertising details (Date Received,Department,Cost,Paper published, Date of publication, Description... etc) can’t you use Trello (free), or a Google Sheet (also free)?
10. Track trademark registration details for which there already is an entire government department, not to mention third-party software (IOlite, IPzen) for large-scale trademark tracking (500 items etc). SPC doesn't have anywhere near as many logos; why does this have to be baked into software?
11. Digital signatures a standard request across departments. I see we’re casually taking on Adobe Docusign / TinyPDF now…
12. *- Facility to view Asset Value,Depriciation,cumulative depriciation,net value after depreciation. - Facility to view debtors details category wise - Facility view SPC debtors details -Name ,Address ,Credit limit ,Bank guarantee with expiry, Registration etc - Facility to view staff debtors details - Loan type, Gurantees,Value, Matuarity date - Facility to view Age Analysis (Handled by Finance department)* Essentially, a bank?
13. Loans, licenses, taxes and rent/lease agreements essentially, landlord software with banking functions stapled on?
14. Prediction “Using sales information able to calculate actual monthly sales, but sales movement is not smooth (quality failure, emergency cases,DHS transfer...etc), therefore can not depend on actual average monthly sales. System should facilitate to handle those situations.” You don’t really need the system to do this for you. In fact, the more variables, the more likely than any pre-baked solution will eventually go disastrously wrong. Given how complex the process is, it would actually be far better to have a competent data scientist on hand who can look directly at the data and make contextual predictions. For example, in times of a fuel crisis, transport is going to be delayed. That’s not something you can account for beforehand, unless you’re magically capable of knowing the future.
15. Creating paper advertisements, publishing to the web, auto-generating invitation and tender letters Have you not heard of Microsoft Word? Canva? Or Google Docs and templates?
16. Prepare meeting agendas and let them record meeting minutes. Instead of, you know, using Notepad.
17. “*Facility to identify subject clerk uniquely Facility to view his work history Facility to identify the work load of clerks at the moment (e.g identify persons with less items… etc)*”. Because why not build a Panopticon while we’re at it, eh? This is project management software: the normal version of this would be JIRA.
18. User define calculation formulas; Uses what-if scenarios to determine if a job can be fulfilled. We’re guessing this came from Microsoft Excel users. Done properly, this amounts to programming language within this system. This can be done with SQL injection, but does anyone at SPC use SQL?
19. Tracking raw materials and packaging used to produce Jeewani. Yes, somewhere in here is also a request for manufacturing support and logistics.

Our first thought was that nobody with technical expertise had looked at this request at all. Rather, we assumed that each department had been told to list the functions they would like to see in their new software, and SPC staff had done so without any thought or consideration as to technological reality.

This assumption was backed up by two things: 1. Overlaps: Many departments overlap and call for identical functionality. Had a technical analyst looked at this, much of the functionality (ie: digital signatures) could have been abstracted to general platform features. 2. Scope: Combined with the extensive inventory management, finance and auditing specs listed here, this software, on the surface of it, this seems something no sane engineer would ever design or build. Even within the Frankenstein’s monster functionality of an ERP, the scope here would be a near-guarantee of failure.

You can do a shit job of everything, but to do this well requires building functionality that AssetPanda and RIB software GMBH have, as well as some functionality that even Lyft doesn’t. Add banking software, Adobe Document Cloud, Auditboard, Atlassian JIRA, Oracle’s NetSuite - an analyst should have been able to look at this and point out the sheer madness at play here. However, someone with technical expertise has clearly looked at this - or rather, rubber-stamped it in a hurry. One of the requests is that this system has to be web-based, without requiring any of the computers at SPC to install anything new, and it has satisfy specific response times - of between 02-05 seconds.

Screen Navigation: screen-to-screen < 3 seconds

Screen Refresh < 2 seconds

Screen list box, combo box < 2 seconds

Screen grid – 25 rows, 10 columns < 3 seconds

Report preview – (all reports) – < 60 seconds in most instances.

Simple search – single table, e5 fields, 3 conditions  < 3 seconds for 100,000 rows

Complex search –a multiple joined table (5), 10 fields, 3 conditions < 5 seconds

for 100,000 rows

Server side validations / computations < 2 milliseconds

Client side validations / computations < 1 millisecond Loading pages < 3 seconds

Saving a record < 5 seconds

Batch processing per 100 records < 120 seconds

Login, authentication, and verification < 5 seconds

From a technical perspective, these are suspiciously specific for a system that supposedly hasn’t existed yet. If these numbers are set in stone, the only way such times can be obtained is if a pre-existing system of some sort exists, and times are pulled from it. The sub-2 ms server-side validation figure looks like it was pulled from [Apache Spark manual, especially for in Continuous Processing](https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html) mode\[2\].

But that stuff is for manuals. The practicality is this: this design is for a web-based piece of software. Speedtest.net suggests that Sri Lanka has a mean latency on wired broadband \~ 25 ms. **You're never going to see this speed. Even Google servers take longer to respond to queries from Sri Lanka.**

## Why is this here? {#h-why-is-this-here}

We’re extrapolating here, but here are some reasonable assumptions: a) this is complete bullshit, taken from manuals written under the most theoretical of conditions, by someone who has no practical experience OR b) SPC is asking for systems faster than Google OR c) either SPC or one of its vendors have broken the laws of physics altogether OR d) or there is an existing system that somehow does the above, and this is a nail in the coffin of making sure it only it gets selected, even in the case that the impossible red-flag spec above can be pulled off by someone else.

## Quick math and quick questions {#h-quick-math-and-quick-questions}

And this is where it gets interesting.

The seven billion LKR figure quotes in the COPE hearing comes to approximately 19.5 million USD.

However, we’ve now noted several major software companies worth of functionality. As we noted above, you can do a shit job of everything, but to do this well requires building functionality that AssetPanda (est: $7M revenue) and RIB software GMBH (est $304M revenue) have, as well as some functionality that even Lyft (est: $2.8B revenue) doesn’t. Add 4Park, Adobe Document Cloud and Auditboard (est: $71.5M revenue). Add Oracle Netsuite, Canva, Microsoft Word (or at least, Notepad)… and now, this seven billion rupee figure ($19.5 million) sounds *impossibly* cheap. A Sri Lankan company capable of building all this from scratch would be a mind-blowing powerhouse of geniuses, and possibly have build their own world-class products already. Move over, Facebook.

It’s actually hard to estimate the cost of ERPs, except when they fail.

1. Waste Management (the company) spent $100 million on a botched SAP implementation and subsequently lost another $350 million in potential benefits had the launch been successful. They sued SAP.
2. FoxMeyer Drugs, once, a $5 billion company and the fourth-largest pharmaceutical distributor in the United States, hired Arthur Anderson Consulting to implement SAP(R/3) for $100 million. The implementation was so bad that FoxMeyer went bankrupt.
3. From 1998 to 2005, the US Navy [sunk $1 billion into four different failed ERP systems](https://www.gao.gov/assets/gao-05-858.pdf).
4. Lidl, the German grocery chain, spent [over $580 million dollars](https://www.academia.edu/38205830/Mission_Failure_at_LIDL_But_Actually_What_was_the_Mission?auto=download) and seven years of development, ultimately throwing it all away and going back to their in-house inventory management system.
5. [Nike lost $500 million because of a botched ERP.](https://www.cio.com/article/264637/enterprise-resource-planning-nike-rebounds-how-nike-recovered-from-its-supply-chain-disaster.html)

So, firstly, ERPs are big business. The $19.5 million figure here is again, impossibly cheap by these standards. However, SPC already has at least one known failure: the Rs. 644 million debacle now contested by e-Wis.

They also seem to know that things can be done cheaper: recall the tender to Loons Lab, to replace the existing [“Rs 644 million rupee” system for Rs 100 million](https://www.newswire.lk/2022/06/08/it-industry-responds-to-cope/).

So we now have three critical questions:

1. Who designed this RFP? The government should have been aware of certain crisis indicators - mounting debt, a general crash in tourism and government revenue, and other things that we described in our series on the economy. Was there nobody on hand to understand what the SPC’s core business is (pharmaceutical, and not, for example, parking)?
2. Who checked this RFP before it went public? Was no serious technical audit performed? Was ICTA (which is supposed to do this work) either absent or incompetent? Was there nobody who understood that given the failure of SPC’s previous ERP system, a little caution should be exercised before calling for monolithic surveillance state-level software like this?
3. Who supplied the seven billion figure? Which software company brazenly agreed to develop software that sounds like it can take on multi-billion-dollar software companies? Any sane software engineer who accepts a spec like this must know how easy it is to fail; we can only presume that someone takes on this risk *knowing that they are going to fail.*

## Stupidity or malice? {#h-stupidity-or-malice}

 ![The Court of Foolishness of Gerard de Lairesse. The accused, pursued by Hatred, is led by Calumny, Envy and Perfidy before a judge with donkey ears, surrounded by Ignorance and Suspicion. From WikiMedia Commons.](/images/library/3a558f9f9824.webp)

One of the mental tools we use at Watchdog is Hanlon’s Razor:

**Never attribute to malice that which is adequately explained by stupidity.**

This Razor is a useful tool for operating in information-poor environments, such as the one we find ourselves in.

However, if stupidity, then three parties have been stupid here: 1) The State Pharmaceutical Corporation, for asking for software that can track everything from milk powder to parking spaces to trademarks, instead of focusing on the core of its mandate and expanding slowly from there. 2) ICTA, for having passed on this. 3) The software vendors who bid for this, who as profit-making companies should have known after one read exactly how bad this was.

The alternate hypothesis is that this is malice: a deliberately bloated white elephant of a software project doomed to go the same way as the last.

However, our word is not the final word in this. While we do our due diligence, and know a fair bit about building software and working with data, we’re not all-knowing arbiters. In that spirit, we’d like to invite you to read the technical requirements for yourself - along with our comments - and judge for yourself. Here is our Google Sheet:

[https://docs.google.com/spreadsheets/d/1Bt9cM_jorJsklOKrhkYbE6-1nUwATPIwqU_u-xyZGI0/edit?usp=drivesdk](https://docs.google.com/spreadsheets/d/1Bt9cM_jorJsklOKrhkYbE6-1nUwATPIwqU_u-xyZGI0/edit?usp=drivesdk)

## Footnotes {#h-footnotes}

\[1\] Disclosure: we were invited because of our work on Elixir, but were unable to attend due to 2/3rds of our technical capacity being in Nepal at the time of writing, working on a set of international investigations.

\[2\] The figures looked familiar because I’ve used Spark before for big data work — think millions and billions of records — for academic research at LIRNEasia.
