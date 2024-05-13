import './GenerateSets.css';
import SettingsForm from './SettingsForm.js'

function GenrateSets() {
  return (
    <div className='generate-sets'>
      <h1>Generate Sets</h1>
      <p>
          We help you create sets of boxes that fit your storage needs!
          Enter your space requirements bellow and click "Generate".
      </p>
      <SettingsForm></SettingsForm>
    </div>
  );
}

export default GenrateSets;