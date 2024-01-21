import { useState } from 'react'

import './App.css'
import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Button } from "@/components/ui/button"
import { quantum } from 'ldrs'
import mascot from './assets/mascot.png'

import ReactPlayer from 'react-player/youtube'
import Reels from './components/reels'
import Test_swipe from './components/test_swiper'
import axios from 'axios';
// import test_vid from '../../backend/videos/0aa43d3c-2731-49bb-8d1e-3918d428a8f8.mp4'



function App() {
  const [loading, setloading] = useState<boolean>(false);
  const [reels, setreels] = useState<string[]>([]);
  const [text, settext] = useState("");
  
  quantum.register()

    

  const handleClick = () => {
    setloading(true)
    axios.post('http://127.0.0.1:8000/generate', {
      q: text
    }).then((response) => {
      console.log("out");
      axios.get('http://127.0.0.1:8000/videos').then((response) => {
        console.log("in");
        const new_url =  response.data.map((video:string)=>{
          return "http://127.0.0.1:8000/videos/"+video
        })
        setreels(new_url)
        setloading(false)
       
        
      }
      ).catch((error) => {
        console.log(error);
      });




      

    }
    ).catch((error) => {
      console.log(error);
    });
    
  }

  return (
    <>
    
    <div className="flex flex-col items-center justify-center min-h-screen top-0 bottom-0 ">
    {reels.length <=0 ? <div>

      {!loading ? 
      <div className='flex flex-col items-center'>

        <h1 className='text-6xl font-montserrat font-bold bg-gradient-to-r from-[#2af0ea] to-[#fe2858] inline-block text-transparent bg-clip-text'> BrainRot+  
      </h1>
      <p className='text-2xl font-montserrat font-semibold '>Don't let tiktok's rot your brain </p>
      </div>
      :
      <div></div>
      }
     

      {loading ? 
      
      <div className='flex flex-col justify-center items-center '>
        <l-quantum
  size="45"
  speed="1.75" 
      color="#00f2ea" 
></l-quantum>

        <p className='mt-5 font-montserrat text-zinc-800 font-semibold text-2xl'>Loading your 🧠 brain 🧟 rot content... </p>



      </div>
      :
      <div>
        <div className="w-full max-w-md p-8 space-y-8 bg-white rounded-xl shadow-lg dark:bg-gray-800">
        <h2 className="text-xl font-montserrat font-medium text-center text-gray-900 dark:text-white">Enter Any Text You Like</h2>
        <p className="text-center font-montserrat text-gray-500 dark:text-gray-400">
          input a text of a chapter of a book or difficult concept 
        </p>
        <div className="grid gap-6">
          <div className="grid w-full gap-1.5">
            <Label className='text-left font-montserrat mb-1' htmlFor="text-input">Enter Text</Label>
            <Textarea id="text-input" placeholder="Type or paste your text here." onChange={
              (e)=>{
                settext(e.target.value)
              }
            }/>
             
          </div>
        </div>
        <Button disabled={text==""} className="w-full font-montserrat hover:bg-[#ff0050]" onClick={()=>{
          handleClick()
}}>Submit</Button>
      
      
      
      </div>

      <div className='mt-8 flex flex-col items-center'>
                        <img className='w-28 h-28' src={mascot} alt="" />
                        <p className='text-sm font-montserrat text-zinc-400'>Built with love ❤️ by burdened bears</p>

      </div>
      </div>
      
       
      
      
      }

        
      </div>:
           <Reels videos={reels}></Reels>

      }
    
   
        </div>



    
    </>
  )
}

export default App
