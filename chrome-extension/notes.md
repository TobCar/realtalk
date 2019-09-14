# How Extensions Work

1. All the configuration of the extension is done in **manifest.json**
2. The **Background script** is the extension's **Event Handler**
* Containing listeners for browser events important to the extension
* It lies dormant until an event is fired then performs the instructed logic
3. Extensions can **tabs.create** or **window.open** 
4. An extension using a page action and popup can use the **declarative action api**
* Setting rules for background scripts when popup is available to users
* When conditions are met, the background script communicates with the popup to make it's icon clickable
5. The **Content Scripts** are used to read or write to webpages
* Containing Javascript that executes in the context of a page that has been loaded into browser
* Reading/Modifying the DOM of webpages the browser visits 
6. The **Options Page** enables customization of the extension
7. Keep in mind most APi methods are **asynchronous** and thus be handled accordingly
8. Extensions can **save data** using the **web storage api**
9. There's a lot of data in **tab object** such as ".incognito, .url,"

# Goal

An extension that onplay it sends:
- Video tag
- Video ID from URL
- Entire URL

# Plan

1. background script waits for user to go onto youtube video

# Testing plan

1. Console.log on background event dispatch 
