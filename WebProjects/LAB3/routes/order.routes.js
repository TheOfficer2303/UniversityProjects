var express = require('express');
var router = express.Router();
const db = require('../db/index.js');

router.get('/', async (req, res) => {

    let [categories, products] = await Promise.all([
        db.query("SELECT * FROM categories"),
        db.query("SELECT * FROM inventory")
    ]
    )

    for (const category of categories.rows) {
        let helper = []
        for (const item of products.rows) {
            // console.log(item);
            
            if (item.categoryid === category.id) {
               helper.push(item);

            }
            
        }
        category.products = helper;
    }

    for (const category of categories.rows) {
        console.log(category.products.length)
    }
    // console.log(categories.rows.items);

    res.render('order', {
        title: 'Order',
        linkActive: 'order',
        categories: categories.rows
    })
})


module.exports = router;