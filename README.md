# Bible Verse Web serive
A REST Api for bible verses, only the KJV in implemented. ReactJs example app using the service: [Check the app](https://4q53xqpo60.codesandbox.io/)

Using Databases from: [https://github.com/scrollmapper/bible_databases] and use the link for reference about the database structure

**Endpoints**
```
::[PORT]/books  # Get list of books
::[PORT]/read?from=1001002&to=1001008
::[PORT]/read?book=1&chapter=1
```
**Setup**

```
pip install -r requirements.txt
python app.py
```
