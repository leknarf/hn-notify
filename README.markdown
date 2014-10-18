HN Notify tells you when it's a good time to post on hacker news. See it in action on [HN Notify](http://hnnotify.leknarf.net).

# Concept

Assuming you want your HN submission to reach the front page, then it's important to post at times when scores on the new page are relatively high compared to the front page.

# Differences from HN Pickup
This project was inspired by [HN Pickup](https://github.com/entaroadun/hnpickup), but differs in a few notable ways:

 - There is a [twitter feed](https://twitter.com/HNNotify), which you can follow to receive alerts.
 - This uses the [Official Hacker News API](https://github.com/HackerNews/API) as its data source, which was only recently published.
 - Instead of calculating an average, this compares the second-highest score on the new page and the second-lowest score on the front page.
 - The chart updates in real-time.
