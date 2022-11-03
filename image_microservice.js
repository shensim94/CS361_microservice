'use strict';

const PORT = 3000;
const express = require("express");
const app = express();

const credentials = require('./credentials.json')
const {google} = require('googleapis')
const customsearch = google.customsearch('v1')

app.use(express.urlencoded({
    extended: true
}));

app.use(express.static('public'));

async function customSearch(keyword){
    const res = await customsearch.cse.list({
        q: keyword,
        searchType: "image",
        num: 10,
        auth: credentials.api_key,
        cx: credentials.cx
    });
    let urls = [];
    res.data['items'].forEach(item => urls.push(item['link']));
    return urls;
}
app.get("/search", async (req, res) => {
    console.log(req.query);
    if (req.query["keyword"]){
        let result = await customSearch(req.query["keyword"]);
        //console.log(result)
        res.send(result);
    }
    else{
        res.send("")
    }
});

// Note: Don't add or change anything below this line.
app.listen(PORT, () => {
    console.log(`Server listening on port ${PORT}...`);
});