import ReactPlayer from "react-player";
import { Separator } from "./ui/separator";
import video from "@/assets/out-15.1.mp4"
import { useState } from "react";
import { set } from "date-fns";
import { X } from "lucide-react";
import { Swiper, SwiperSlide } from 'swiper/react';
    
const Reels = () => {
    
    const [singleViewer, setsingleViewer] = useState(true);
    return ( 

        <>

        {!singleViewer ?
           <div className="flex flex-col justify-center">
            <div className="mb-6">
                <h1 className="font-montserrat text-2xl font-bold">Enjoy your new brain rot content ✨</h1>
                <Separator className="mt-4" />
            </div>
             <div className="grid grid-cols-3 gap-6">
            <div className=" w-[240px] h-[320px] aspect-w-4 aspect-h-3 rounded-md bg-zinc-400">
                     <video 
                      className=" absolute top-0 left-0 w-full h-full object-cover rounded-md hover:cursor-pointer"
                src={video}
                 muted={true} loop={true} 
                 onMouseOver={(e) => e.currentTarget.play()}
                    onMouseOut={(e) => e.currentTarget.pause()}
                    onClick={()=>{setsingleViewer(!singleViewer)}}
                ></video>


                     
                
              


            </div>

      
          
           
            


        




        </div>
                        <Separator className="mt-4" />


        </div>:
         <div className="w-full h-screen overflow-hidden overscroll-none bg-zinc-900">
                <X className=" text-white bg-zinc-700 fixed w-10 h-10 mt-2 ml-2 hover:bg-slate-800 p-2  rounded-full" onClick={()=>{setsingleViewer(!singleViewer)}}/>

                <div className="flex flex-col items-center mt-8">
                     <div className="min-aspect-w-4 min-aspect-h-3 rounded-md bg-zinc-400">
                     <video 
                      className=" object-cover rounded-md hover:cursor-pointer"
                src={video}
                 muted={true} loop={true} 
                 onMouseOver={(e) => e.currentTarget.play()}
                    onMouseOut={(e) => e.currentTarget.pause()}
                    onClick={()=>{setsingleViewer(!singleViewer)}}
                ></video>


                     
                
              


            </div>

                </div>





        </div>

        
    
    }
      



       
        
        </>
       
       
     );
}
 
export default Reels;