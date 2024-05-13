import { /*useEffect,*/ useState, useRef } from 'react';
import './GenerateSets.css';
import DisplayGeneratedSets from './DisplayGeneratedSets.js'
import api from '../../api/ApiConnection';
import { HttpStatusCode } from 'axios';

const SettingsForm = () => {
  // "useRef" hook was used to avoid unnecessary re-renderings
  // It stores the list of sets returned by the generator
  const [generatedSets, setGeneratedSets] = useState();
  
  // It stores the length of the container
  const lengthRef = useRef(0);
  // It stores the width of the container
  const widthRef = useRef(0);
  // It stores the height of the container
  const heightRef = useRef(0);

  // It stores the unit that the container is measured in
  const unitRef = useRef("cm");

  // It stores the desired number of boxes in a set
  const numRef = useRef(0);

  // It stores the type of container where the boxes will be placed
  const containerTypeRef = useRef("shelf");

  // NOTE: this is relative to the previous version
  // "useState" hook was used so that the total number of boxes ("num") can be updated live
  // TODO: In the future, one should think of a better solution. Maybe split the form into separate components
  // It stores the number of boxes that fit across the container's length 
  // const [numLength, setNumLength] = useState();
  // // It stores the number of boxes that fit across the container's width 
  // const [numWidth, setNumWidth] = useState();
  // // It stores the number of boxes that fit across the container's height 
  // const [numHeight, setNumHeight] = useState();
  // // It stores the total number of desired boxes
  // const [num, setNum] = useState(0);

  // Flag that indicates whether new products are being loaded
  const [loading, isLoading] = useState(false);
  // It signals an error
  const [error, hadError] = useState(false)

  // NOTE: this is relative to the previous version
  // "useEffect" hook to update the total number of boxes ("num") as the values are updated
  // useEffect(() => {
  //   setNum(numLength * numWidth * numHeight);
  // }, [numLength, numWidth, numHeight]);

  // Function to get the generated sets
  const getProductSets = async () => {
    isLoading(true);
    hadError(false);

    try{
      // Parsing Refs' values
      const length = parseFloat(lengthRef.current.value);
      const width = parseFloat(widthRef.current.value);
      const height = parseFloat(heightRef.current.value);

      const unit = unitRef.current.value;

      const num = parseInt(numRef.current.value);

      const containerType = containerTypeRef.current.value;

      // Configurations used in set generation
      const configurationBodyData = {
        n: num,
        container_type: containerType,
        //layout: [numLength, numWidth, numHeight], 
        container_dimensions: [length, width, height],
        unit: unit
      };

      // Request parameters
      const configurationParameters = {
        method: "GET",
        headers: { 
            'Content-Type' : 'application/json' 
        }
      }
      // API call
      // NOTE: At the moment, it is only possible to send body data (via browser) in "POST" requests
      const response = await api.post("/get-product-sets/", configurationBodyData, configurationParameters);
      /*------------------------------------------*/
      // Debug: statement to test loading
      //await new Promise(r => setTimeout(r, 2000));
      /*------------------------------------------*/

      // If the request was successful (200)
      if (response.status === HttpStatusCode.Ok) {
        // Updates the sets, according to the fetched data
        // If it is not possible to generate any sets, the endpoint returns an empty list
        setGeneratedSets(response.data)

        // Product loading ends here
        isLoading(false);
      }
      // In case of an error, a message is displayed
      else {
        isLoading(false);
        hadError(true);

        setGeneratedSets()
        console.error(`Error: code ${response.status}!`);
      }
    }
    // Catches exceptions occurred in during the API call
    catch (e) {
      isLoading(false);
      hadError(true);

      // Updates "generatedSets" to undefined, so that an error message is displayed
      setGeneratedSets()

      console.error(`Error: ${e.message}!`);
    }
  }

  // Function that verifies if a certain number of boxes is within the acceptable range
  const boxNumberValidation = (boxNumber, max) => {
    if (boxNumber >= 1 && boxNumber <= max) {
      return true;
    }
    return false;
  }

  // NOTE: this is relative to the previous version
  // Function to validate layout-related inputs
  // const layoutValidation = (layout, maxPerAxis, maxTotal) => {
  //   if(layout[0] * layout[1] * layout[2] <= maxTotal && 
  //       boxNumberValidation(layout[0], maxPerAxis) &&
  //       boxNumberValidation(layout[1], maxPerAxis) &&
  //       boxNumberValidation(layout[2], maxPerAxis)) {
  //     return true;
  //   }
  //   return false;
  // }

  // Function used to check if a given dimension is witin the allowed values
  const dimensionValidation = (dim, max) => {
    if (dim > 0 && dim <= max) {
      return true;
    }
    return false;
  }

  // Function to validate the volume-related inputs
  const volumeValidation = (dims, maxPerAxis, maxVolume) => {
    if (dims[0] * dims[1] * dims[2] <= maxVolume && 
          dimensionValidation(dims[0], maxPerAxis) &&
          dimensionValidation(dims[1], maxPerAxis) &&
          dimensionValidation(dims[2], maxPerAxis)) {
      return true;
    }
    return false;
  }

  // Main function to validate the form
  const formValidation = () => {
    const lRef = lengthRef.current.value;
    const wRef = widthRef.current.value;
    const hRef = heightRef.current.value;

    const nRef = numRef.current.value;

    // NOTE: this is relative to the previous version
    // Checks if all inputs are numbers
    // if (isNaN(numLength) || isNaN(numWidth) || isNaN(numWidth) || isNaN(lRef) || isNaN(wRef) || isNaN(hRef)) {
    //   return false;
    // }
    
    // Checks if all values are within the established thresholds
    // TODO: Change superior limits
    return boxNumberValidation(nRef, 10) && volumeValidation([lRef, wRef, hRef], 150, 1000000);

    // NOTE: this is relative to the previous version
    // return layoutValidation([parseInt(numLength), parseInt(numWidth), parseInt(numHeight)], 10, 10) && volumeValidation([lRef, wRef, hRef], 150, 1000000); 
  } 

  // Function that handles the submission
  const handleSubmit = (event) => {
    event.preventDefault();

    // TODO: Validate the form live, AS VALUES CHANGE
    // Validates the form before fetching data
    if (formValidation()) {
      getProductSets();
    }
    // It displays an alert if any of the inputs are not valid, or if they are not within the thresholds
    else {
      alert("Error: Invalid data!\nHint: Maximum of 10 boxes in a maximum of 1m³/35.315ft³");
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="length"
          placeholder="Length"
          ref={lengthRef}
        />
        <input
          type="text"
          name="width"
          placeholder="Width"
          ref={widthRef}
        />
        <input
          type="text"
          name="height"
          placeholder="Height"
          ref={heightRef}
        />

        <select ref={unitRef}>
          <option value="cm">cm</option>
          <option value="in">in</option>
        </select>

        <input
          type="text"
          name="n-boxes"
          placeholder="Number of boxes"
          ref={numRef}
        />

        <select ref={containerTypeRef}>
          <option value="shelf">shelf</option>
          <option value="drawer">drawer</option>
        </select>

        {/* NOTE: this is relative to the previous version*/}
        {/* <input
          type="text"
          name="n-length"
          placeholder="Number of boxes in length"
          value={numLength || ""}
          onChange={(event) => setNumLength(event.target.value)}
        />
        <input
          type="text"
          name="n-width"
          placeholder='Number of boxes in width'
          value={numWidth || ""}
          onChange={(event) => setNumWidth(event.target.value)}
        />
        <input
          type="text"
          name="n-height"
          placeholder="Number of boxes in height"
          value={numHeight || ""}
          onChange={(event) => setNumHeight(event.target.value)}
        />
        <p>
          Number of boxes: {num ? num : 0}
        </p> */}

        <button type="submit">Generate</button>
      </form>

      {
        loading || error ?
          <p>
          {loading && "Loading"}
          {error && "Error!"}
          </p>
        :
          <div>
            {generatedSets ? <DisplayGeneratedSets generatedSets={generatedSets}></DisplayGeneratedSets> : <div></div>}
          </div>
      }
    </div>
  );
}

export default SettingsForm;