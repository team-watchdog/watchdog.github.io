---
layout: post
title: Postmortem
description: We made a mistake. Here's what happened and here's how we're fixing it.
date: 2019-09-17
author: yudha
image: '/images/articles/postmortem/main.jpg'
tags: [investigation, healthcare]
tags_color: '#835F46'
---
by [Yudhanjaya Wijeratne](/authors/yudha)

On September 15th 2019, at 7:04:41 pm, we published a news update titled “Accident on Southern Expressway - so far 16 people dead on the spot and 1 dead in Colombo.”

In reality, that wasn’t what happened. In reality 6 vehicles collided on the highway, blocking  both Lanes from Matara to Kadawatha for a while. 2 people were hospitalized.  Drivers were advised to lower their speed to 60KMPH during rainy weather. [1] [2]

We checked with the traffic police, issued an update with the right facts, and fired off an apology, but the fact remains that at that point we had published a major piece of fake news, and people were understandably pissed off.

![Sanjiva]({{site.baseurl}}/images/articles/postmortem/second.jpg)


## WHAT WENT WRONG?

As far as we can trace the issue, here’s what happened:

  1. Factchecker A was on a bus on a trip when everyone received a Whatsapp notification of the rumor that 16 people had died (possibly a bastardization of an earlier accident [3]). This was around 15:00 PM.

  2. Since A was off duty at this point, they called Factchecker B, who checked our sources. There was nothing there, so they waited for two hours and checked again. At this point we had received multiple pings on the same rumor.

  3. There was confirmation that an accident had happened on the highway (but not that 16 people had died). Factchecker B then made the cardinal error of publishing the information, except instead of the confirmation of the accident they ended up typing the rumor in full and publishing it at 17:04 PM.

  4. Factchecker C, who was on the highway at the time, promptly hit the brakes, almost triggered an actual highway accident, and then proceeded to check out the rumor in more detail. On finding that it was false, they called the others on the team, and all hell broke loose

## WHAT DID WE LEARN?

We have a set procedure on how we do things. Every rumor we get we check against Azzam Ameen of BBC Sinhala, Marianne David of the DailyFT, Roel Raymond of Roar, then Newsfirst and Derana. If they don’t have anything, we scale to a larger, secondary list of journalists and news channels - which includes calling people up and bugging them, and asking them to update in public so we have a clear, publicly visible source to link to. On rare occasions we dig into it ourselves - like checking with the police.

We understand that every source has their biases, so our rule is we say absolutely nothing until at least three unrelated sources confirm a given piece of news.

The protocol didn’t fail (this was our first fear: that somehow enough of our sources were compromised as to overwhelm the truth). It came down to simple human error.

Human error happens and is unavoidable. So we’re reinforcing our policies with our platform tools, internally.  As part of our new update to WatchDog, we will include the following feature to all news updates:




Every post will have to have a primary source and a secondary source linked.

In instances of manual verification (what we call investigations), the rumor has to be on our investigations list, and the entire process of verification documented in detail so that anyone can see how it was validated.

We’ve added restrictions on our backend so that there’s absolutely no way to publish without entering this information. The process is forced every time. That should make us think twice. We will be releasing a new version of our mobile apps in a couple of days that contains all of this stuff.

We’ve also:

  1. Made the decision to archive the content of original sources in case someone takes down their story without issuing a redaction.
  2. Re-evaluated our list of sources (just in case) and basically set it in stone: to add a new source to the list is a much more difficult process now, and requires a vote among multiple members.

We appreciate our users for keeping us accountable. Many of you have called / messaged us to assure us that, basically, shit happens and flowers grow on it. But in reality we should have accounted for human error. While no tech solution is 100% proof - as Terry Pratchett once said, human stupidity beats artificial intelligence every time - we hope that the checks we’ve put into place will make us better at doing what we set out to do.

Yours,

Team Watchdog.

References:

[1] [https://www.newsfirst.lk/2019/09/15/six-vehicles-collide-with-each-other-along-the-southern-expressway/](https://www.newsfirst.lk/2019/09/15/six-vehicles-collide-with-each-other-along-the-southern-expressway/)

[2][http://www.hirunews.lk/224332/6-vehicles-collide-on-the-southern-expressway](http://www.hirunews.lk/224332/6-vehicles-collide-on-the-southern-expressway)

[3] [http://www.sundaytimes.lk/article/1079349/one-dead-19-injured-in-accident-near-southern-expressway](http://www.sundaytimes.lk/article/1079349/one-dead-19-injured-in-accident-near-southern-expressway)
