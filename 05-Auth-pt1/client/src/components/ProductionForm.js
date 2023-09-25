import React, {useState} from 'react'
import styled from 'styled-components'
import { useHistory } from 'react-router-dom'
const initialState = {
  title: '',
  director: '',
  budget: '',
  description: '',
  genre: '',
  image: '',
}

function ProductionForm({ addProduction }) {

  const [ formState, setFormState ] = useState( initialState )
  const [ errors, setErrors ] = useState( null )

  const updateFormState = event => {
    const { name, value } = event.target
    const newFormState = { ...formState, [ name ] : value }
    if ( name == 'budget' ) {
      newFormState.budget = parseFloat( newFormState.budget )
    }
    setFormState( newFormState )
  }
  
  const history = useHistory()

  const createNewProduction = ( event ) => {
    event.preventDefault()

    const postRequest = {
      method: 'POST',
      headers: {
        'content-type': 'application/json',
        'accept': 'application/json'
      },
      body: JSON.stringify( formState )
    }

    fetch( '/productions', postRequest )
    .then( r => r.json() )
    .then( new_prod_data => {
      if ( new_prod_data.errors ) {
        setErrors( new_prod_data.errors )
      }
      else {
        setErrors( null )
        addProduction( new_prod_data )
      }
    })
  }
  
  return (
    <div className='App'>
      { errors ? 
        <div>
          { errors.map( error => <li style={{ color: 'red' }}>{error}</li> ) }
        </div> : null }
      <Form onSubmit={ ( event ) => createNewProduction( event ) } >
        <label>Title </label>
        <input type='text' name='title' value = { formState.title } onChange={ updateFormState } />
        
        <label> Genre</label>
        <input type='text' name='genre' value = { formState.genre } onChange={ updateFormState } />
      
        <label>Budget</label>
        <input type='number' name='budget' value = { formState.budget } onChange={ updateFormState }/>
      
        <label>Image</label>
        <input type='text' name='image' value = { formState.image } onChange={ updateFormState } />
      
        <label>Director</label>
        <input type='text' name='director' value = { formState.director } onChange={ updateFormState }/>
      
        <label>Description</label>
        <textarea type='text' rows='4' cols='50' name='description' value = { formState.description } onChange={ updateFormState }/>
      
        <input type='submit' />
      </Form> 
    </div>
  )
}
  
export default ProductionForm

  const Form = styled.form`
    display:flex;
    flex-direction:column;
    width: 400px;
    margin:auto;
    font-family:Arial;
    font-size:30px;
    input[type=submit]{
      background-color:#42ddf5;
      color: white;
      height:40px;
      font-family:Arial;
      font-size:30px;
      margin-top:10px;
      margin-bottom:10px;
    }
  `