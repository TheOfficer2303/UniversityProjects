var express = require('express');
var router = express.Router();
const db = require('../db/index.js');

router.get('/:id([0-9]|[1-9][0-9])', async (req, res) => {
    let [categories, products] = await Promise.all([
        db.query("SELECT * FROM categories"),
        db.query("SELECT * FROM inventory"),
       
    ]
    )

    let id = parseInt(req.params.id);
    
    let product, categoryToSend, suppliersToSend;

    for (const item of products.rows) {
        if (item.id === id) {
            product = item; 
        }
    }    
    
    if (product) {
        for (const category of categories.rows) {
            if (product.categoryid === category.id) {
                categoryToSend = category;
            }
        }

        let [suppliers] =  await Promise.all([
            db.query(`SELECT DISTINCT * FROM suppliers WHERE supplierfor = ${id}`)
        ])
        suppliersToSend = suppliers.rows;
        console.log(supplierLength = suppliersToSend.length);
        res.render('item', {
            title: product.name,
            linkActive: 'order',
            item: product,
            category: categoryToSend,
            suppliers: suppliersToSend
        })
    } else {
        res.status(404).send("AAAAAAAAAA nema ništa ovdje.");
    }

    
})

router.get('/:id([0-9]|[1-9][0-9])/editsupplier/:sid([0-9]|[1-9][0-9])', async (req, res) => {
    let sid = parseInt(req.params.sid);
    console.log("sid:", sid);

    let supplier = await db.query(`SELECT * FROM suppliers WHERE id = ${sid}`)
    
    res.render('predlozak', {
        linkActive: "order",
        supplier: supplier.rows[0]
    })
})

router.post('/:id([0-9]|[1-9][0-9])/editsupplier/:sid([0-9]|[1-9][0-9])', async function (req, res) {
    console.log(req.body);

    let errors = [];
    let errDB = "";
    let itemID = req.params.id;
    let supplierID = req.params.sid;


    let name = req.body.name;
    
    if (name.trim().length < 2 || name.trim().length > 22) {
        let error = {
            msg: "Invalid value",
            param: "name"
        }

        errors.push(error);
    }

    let country = req.body.country;
    if (country.trim().length < 2 || country.trim().length > 22) {
        let error = {
            msg: "Invalid value",
            param: "country"
        }

        errors.push(error);
    }


    let county = req.body.county;
    if (county.trim().length < 2 || county.trim().length > 22) {
        let error = {
            msg: "Invalid value",
            param: "county"
        }

        errors.push(error);
    }

    let email = req.body.email;
    if(!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        let error = {
            msg: "Invalid value",
            param: "email"
        }

        errors.push(error);
    }

    let years = req.body.years;
    if(years < 1945 || years > 2021) {
        let error = {
            msg: "Invalid value",
            param: "suppliersince"
        }

        errors.push(error);
    }

     if (errors.length === 0) {
        try {
            await Promise.all([
                 db.query(`UPDATE suppliers SET name = '${name}', 
                 country = '${country}', county = '${county}', 
                 email = '${email}', suppliersince = '${years}'
                 WHERE id = ${supplierID}`)
             ])
         } catch (err) {
             errDB = err.message;
         }
    }
    
    res.render("error", {
        title: "Error",
        linkActive: "order",
        errors: errors.length === 0 ? 'none' : errors,
        itemID: itemID,
        errDB: errDB === "" ? 'no error' : errDB
    })

})

module.exports = router;
