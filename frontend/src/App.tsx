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



function App() {
  const [loading, setloading] = useState<boolean>(false);
  const [reels, setreels] = useState([]);
  quantum.register()

  return (
    <>
    
    <div className="flex flex-col items-center justify-center min-h-screen top-0 bottom-0 ">
      {/* {!loading ? 
      <div>

         <h1 className='text-6xl font-montserrat font-bold bg-gradient-to-r from-[#2af0ea] to-[#fe2858] inline-block text-transparent bg-clip-text'> BrainRot+  
      </h1>
      <p className='text-2xl font-montserrat font-semibold'>Don't let tiktok's rot your brain </p>
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
        <h2 className="text-xl font-montserrat font-medium text-center text-gray-900 dark:text-white">Upload your PDF or Enter Text</h2>
        <p className="text-center font-montserrat text-gray-500 dark:text-gray-400">
          We accept both PDF files and direct text input. Choose the method that works best for you!
        </p>
        <div className="grid gap-6">
          <div className="grid w-full gap-1.5">
            <Label className="text-left font-montserrat" htmlFor="pdf-upload">Upload PDF</Label>
            <Input accept=".pdf" id="pdf-upload" type="file" />
          </div>
          <div className="grid w-full gap-1.5">
            <Label className='text-left font-montserrat' htmlFor="text-input">Or Enter Text</Label>
            <Textarea id="text-input" placeholder="Type or paste your text here." />
          </div>
        </div>
        <Button className="w-full font-montserrat hover:bg-[#ff0050]" onClick={()=>setloading(true)}>Submit</Button>
      </div>

      <div className='mt-8 flex flex-col items-center'>
                        <img className='w-28 h-28' src={mascot} alt="" />
                        <p className='text-sm font-montserrat text-zinc-400'>Built with love ❤️ by burdened bears</p>

      </div>
      </div>
      
       
      
      
      } */}
     <Reels></Reels>
        </div>



    
    </>
  )
}

export default App
