# poe-headhunter-tracker


Simple bot to track and report headhunter prices below a threshold through email.

This bot tracks listings from the [official POE trade website](https://www.pathofexile.com/trade).

![alt text](assets/headhunter_tooltip.png)

# How to use

Adjust the details in `config.json`:
- League
- Currency threshold
- Email address and server
- Item name
- User agent (Cannot access POE trade API without specification)

The bot can technically handle any item query, but is currently built primarily for headhunter price scraping and reporting.

# Dependencies

