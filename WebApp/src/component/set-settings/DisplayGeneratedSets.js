import './GenerateSets.css';

const DisplayGeneratedSets = ({generatedSets}) => {
  return (
    <div>
      {
        generatedSets.length !== 0 ?
          <div>
            {
              generatedSets.map((p_set, idSet) => (
                <div key={idSet}>
                  <p>Wasted Percentage: {(p_set.wasted_volume_fraction*100).toFixed(3)}%</p>
                  {p_set.product_list.map((product, idProduct) => (
                      <div key={idProduct}>
                        <img src={product.image_source} width={50} height={50} alt={product.url}></img>
                        <p>{product.name}: {product.length}x{product.width}x{product.height}</p>
                      </div>
                  ))}
                  <p>------------------</p>
                </div>
              ))
            }
          </div>
        :
          <p>Nothing to show here!</p>
      }
    </div>
  );
}

export default DisplayGeneratedSets;