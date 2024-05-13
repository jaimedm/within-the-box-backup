import './App.css';
import About from './about/About';
import GenrateSets from './set-settings/GenerateSets';
import Products from './products/Products';

function App() {
  return (
    <div className='app-content'>
      <nav className='nav-bar'>
        <h1><a href='/#'>WithinTheBox</a></h1>
      </nav>

      <About></About>
      <GenrateSets></GenrateSets>
      {/*Code splitting the section of boxes-only loaded when we have the sets-->*/}
      <Products></Products>
    </div>
  );
}

export default App;
