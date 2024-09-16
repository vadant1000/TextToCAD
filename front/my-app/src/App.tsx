import './App.css';
import axios from 'axios';
import { useEffect, useState } from 'react';
import { Crypto } from './Types';
import { FormEvent } from 'react';
import {StlViewer} from "react-stl-viewer";

const style = {
  top: 0,
  left: 0,
  width: '75vw',
  height: '75vh',
  
}



function App() {
    const [cryptos, setCryptos] = useState<Crypto[] | null>(null);
    const [selected, setSelected] = useState<Crypto>({params: [],name: '', id: ''});
    const [formdata, setFormdata] = useState<any>({});
    const [viewer, SetViewer] = useState(false);
    
    useEffect(() => {
        const url =
            'http://127.0.0.1:8000/visual/';
        axios.get(url).then((response) => {
            setCryptos(response.data);
            
        });
    }, []);

    
const handleChange = (e:FormEvent<HTMLFormElement>) => {
  const target = e.target as HTMLInputElement
  setFormdata({id: selected.id, ...formdata, [target.name]: target.value })
}  



const handleSubmit = (e:FormEvent<HTMLFormElement>) => {
  e.preventDefault()
  const method = 'GET';
  const url = 'http://127.0.0.1:8000/detail/';
  console.log(formdata)
  axios.post('http://127.0.0.1:8000/visual/', formdata).then(response =>{
    SetViewer(true);
    axios
      .request({
        url,
        method,
        responseType: 'blob', //important
      })
      .then(({ data }) => {
        const downloadUrl = window.URL.createObjectURL(new Blob([data]));
        const link = document.createElement('a');
        link.href = downloadUrl;
        link.setAttribute('download', 'detail.stl'); //any other extension
        document.body.appendChild(link);
        link.click();
        link.remove();
      });
    }
  )
  setFormdata({})
  
  
}  
    return (
        <>
            
                <select onChange={(e) => {const c = cryptos?.find((x) => x.id === e.target.value ) as Crypto; setSelected(c);}}>

                    {cryptos
                        ? cryptos.map((crypto) => {
                              return (
                                  <option key={crypto.id} value={crypto.id}>
                                      {crypto.name}
                                  </option>
                              );
                          })
                        : null}
                </select>
          
            

            <form onChange={e => handleChange(e)} onSubmit={(e) => handleSubmit(e)}>
              {selected.params.map((param:any,index:number) => {
                return( <input key={index+'input'} placeholder={param} name={param}></input>);
              })}
              <button type='submit'>Visual</button>
            </form>
            {viewer && (<div className='mydetail'><StlViewer style={style} orbitControls shadows url= "http://127.0.0.1:8000/detail/?make=1"/></div>)}
            
          
        </>
    );
}

export default App;