import React, { useState, useEffect } from 'react'
import styled from 'styled-components'
import { useHistory, useParams } from 'react-router-dom'


function ProductionEdit({updateProductions, production_edit, productionsUrl}) {
  const [ production, setProduction ] = useState(
    {
      title: '',
      director: '',
      budget: '',
      description: '',
      genre: '',
      image: '',
    }
  )
  const [ errors, setErrors ] = useState( null )

  const params = useParams()

  useEffect( () => {
    if ( production_edit )
      setProduction( production_edit )
    else if ( params.id )
      fetch( `/productions/${params.id}` )
      .then( r => r.json() )
      .then( setProduction )
  }, [] )
  
  const updateFormState = event => {
    const { name, value } = event.target
    const newFormState = { ...production, [ name ] : value }
    if ( name == 'budget' ) {
      newFormState.budget = parseFloat( newFormState.budget )
    }
    setProduction( newFormState )
  }
  const history = useHistory()

  const patchProduction = ( event ) => {
    event.preventDefault()

    const patchRequest = {
      method: 'PATCH',
      headers: {
        'content-type': 'application/json',
        'accept': 'application/json'
      },
      body: JSON.stringify( production )
    }

    fetch( `/productions/${ params.id }`, patchRequest )
    .then( r => r.json() )
    .then( updatedProd => {
      if ( updatedProd.errors )
        setErrors( updatedProd.errors )
      else {
        setErrors( null )
        updateProductions( updatedProd )
        history.push( `/productions/${ updatedProd.id }` )
      }
    })
  }
  
  return (
    <div className='App'>
      { errors ? errors.map(error => <li style={{ color: 'red' }}>{error}</li>) : null }
      <Form onSubmit={ patchProduction }>
        <label>Title </label>
        <input type='text' name='title' value={ production.title } onChange={ updateFormState }  />
        
        <label> Genre</label>
        <input type='text' name='genre' value= { production.genre } onChange={ updateFormState }  />
      
        <label>Budget</label>
        <input type='number' name='budget' value={ production.budget } onChange={ updateFormState } />
      
        <label>Image</label>
        <input type='text' name='image' value= { production.image } onChange={ updateFormState }  />
      
        <label>Director</label>
        <input type='text' name='director' value={ production.director } onChange={ updateFormState }  />
      
        <label>Description</label>
        <textarea type='text' rows='4' cols='50' name='description'  value={ production.description } onChange={ updateFormState } />
      
        <input type='submit' />
      </Form> 
    </div>
  )
}
  
export default ProductionEdit

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