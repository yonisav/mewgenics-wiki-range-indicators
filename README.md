# mewgenics-wiki-range-indicators
Range indicators implementation for the mewgenics wiki https://mewgenics.wiki.gg/

Credit to IsaacBee from the wiki for doing most of the CSS and HTML work.

This project is the culmination of my efforts so far, going from the raw game data all the way to a finished product that can be displayed and be helpul to the playerbase on the wiki.
It has 5 main stages:
1. Parsing through the game data (GON files) and extracting the relevant information into relevant classes. Done with Python.
2. Taking the parsed information and building text blocks that can be placed in the wiki. Done with Python using PyWikiBot libraries.
3. Creating templates on the wiki to easily pass the attributes and make it easily useable for non-bots. Done with wiki templtes. https://mewgenics.wiki.gg/wiki/Template:RangeIndicator
4. Craeting a Lua Module for the logic, translationg the atributes into a grid that can ber displayed. Done with Lua. https://mewgenics.wiki.gg/wiki/Module:RangeIndicator

   4.1 Using the GridShape Module made by IsaacBee for building the HTML: https://mewgenics.wiki.gg/wiki/Module:GridShape
5. Creating a CSS custom design to display the indicators of the article in a visually pleasesing way, that resembles the in game UI. Done with CSS. https://mewgenics.wiki.gg/wiki/Template:RangeIndicator/styles.css
