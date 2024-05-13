import { useState, useEffect, useCallback } from 'react';
import './Products.css';
import api from '../../api/ApiConnection';
import { HttpStatusCode } from 'axios';

const ProductList = () => {
    // It stores the list of fetched products
    const [products, setProducts] = useState([]);
    // Flag that indicates whether there are no more products to fetch
    const [finished, isFinished] = useState(false);
    // Flag that indicates whether new products are being loaded
    const [loading, isLoading] = useState(false);
    // It signals an error
    const [error, hadError] = useState(false)
    // It marks the index where the fetch should start
    const [begin, setBegin] = useState(0);

    /*  
        "useCallback" allows passing the function "getProducts" 
        in "useEffect"'s array of dependencies, while avoiding 
        unecessary renderings and possible infinite loops.
        Because the function is memoized (cached), the same 
        function instance will be returned every time the 
        component re-renders.
    */
    // Function which fetches and updates the list of products
    const getProducts = useCallback( async (begin, step) => {
        isLoading(true);
        hadError(false);

        try {
            // API call
            const response = await api.get(`/get-products-by-index/?begin=${begin}&end=${begin + step}`);
            /*------------------------------------------*/
            // Debug: statement to test loading
            //await new Promise(r => setTimeout(r, 2000));
            /*------------------------------------------*/

            // If the request was successful (200)
            if (response.status === HttpStatusCode.Ok) {
                // If the result is not empty, it means we have not reached the end of the product table
                if (response.data.length !== 0) {
                    setProducts((oldproducts) => oldproducts.concat(response.data));
                }
                else {
                    isFinished(true);
                }
                // Product loading ends here
                isLoading(false);
            }
            // In case of an error, a message is displayed
            else {
                isLoading(false);
                hadError(true);
                console.error(`Error: code ${response.status}!`);
            }
        }
        // Catches exceptions occurred in during the API call
        catch (e) {
            isLoading(false);
            hadError(true);
            console.error(`Error: ${e.message}!`);
        }
    }, []);

    // "useEffect" hook to manage updates to the value "begin"
    useEffect(() => {
        getProducts(begin, 9);
    }, [begin, getProducts]);
    
    // Function to handle the logic of scrolling
    const handleScroll = () => {
        /* 
            "window.innerHeight" is the height of the browser window in pixels;
            "document.documentElement.scrollTop" is the number of pixels that the page has been scrolled vertically;
            "document.documentElement.scrollHeight" is the total height of the page in pixels;
            1 pixel of margin is added to make sure one reached the very bottom of the page.
        */
        // If the bottom of the page (end of product list) is reached, AND if there are more products to load, AND if there is no ongoing product fetch
        if ((window.innerHeight + document.documentElement.scrollTop + 1 >= document.documentElement.scrollHeight) && !finished && !loading) {
            // The value of "begin" is updated, which triggers a new product load
            setBegin((begin) => begin + 10);
        }
    }

    // "useEffect" hook to manage scroll events (necessary for loading more products)
    useEffect(() => {
        // Event listener to detect scroll events
        window.addEventListener('scroll', handleScroll);

        // cleanup function
        return () => window.removeEventListener('scroll', handleScroll);
    });

    return (
        <div>
            {
                products.map((product, id) => (
                    <p key={id}>{product.name}</p>
                ))
            }
            <p>
                {loading && "Loading"}
                {finished && "Nothing to show here!"}
                {error && "Error!"}
            </p>
        </div>
                        
    );
  }

export default ProductList;