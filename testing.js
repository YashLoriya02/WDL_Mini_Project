const mongoose = require('mongoose');

mongoose.connect('mongodb://localhost:27017/mobiles', {
    useNewUrlParser: true,
    useUnifiedTopology: true,
});
const db = mongoose.connection;

const productSchema = new mongoose.Schema({
    Name: String,
    Price: String,
    Spec1: String,
    Spec2: String,
    Spec3: String,
    Spec4: String,
    Spec5: String,
    Spec6: String,
    Spec7: String,
    Spec8: String,
    IMG_URL: String,
  });
  
const Product = mongoose.model('Product', productSchema);

const pipeline = [
    {
        $set: {
            Price: {
                $toInt: {
                    $trim: {
                        input: {
                            $replaceAll: {
                                input: '$Price',
                                find: '[^\\d]',
                                replacement: ''
                            }
                        }
                    }
                }
            }
        }
    }
];

Product.aggregate(pipeline)
    .then(result => {
        console.log(`Number of documents updated: ${result.length}`);
    })
    .catch(error => {
        console.error('Error updating documents:', error);
    });
