import ReactPlayer from "react-player";
import { Separator } from "./ui/separator";
import video from "@/assets/out-15.1.mp4"
import { useState,useEffect ,useRef} from "react";
import { set } from "date-fns";
import { X } from "lucide-react";
import { Swiper, SwiperSlide } from 'swiper/react';
import { Card, CardContent } from "@/components/ui/card"
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
  CarouselApi
} from "@/components/ui/carousel" 
import { WheelGesturesPlugin } from 'embla-carousel-wheel-gestures'
import Footer from "./footer";

const Reels = ({videos}:{videos:string[]}) => {
    
    const [singleViewer, setsingleViewer] = useState(false);
    // const [videos, setvideos] = useState([{video:video,play:false},{video:video,play:false},{video:video,play:false},{video:video,play:false}]);
      const [api, setApi] = useState<CarouselApi>()
    const currentVideo = useRef(null)
 
  useEffect(() => {
    if (!api) {
      return
    }
 

    console.log(api.slideNodes())
    console.log(api.slidesInView())
    

    
  }, [api])
    return ( 

        <>

        {!singleViewer ?
           <div className="flex flex-col justify-center">
            <div className="mb-6">
                <h1 className="font-montserrat text-2xl font-bold">Enjoy your new brain rot content ✨</h1>
                <Separator className="mt-4" />
            </div>
             <div className="grid grid-cols-3 gap-6">
              {videos.map((video, index) => (
                       <div key={index} className=" w-[240px] h-[320px] aspect-w-4 aspect-h-3 rounded-md bg-zinc-400">
                     <video 
                      className=" absolute top-0 left-0 w-full h-full object-cover rounded-md hover:cursor-pointer"
                src={video}
                 muted={true} loop={true} 
                 onMouseOver={(e) => e.currentTarget.play()}
                    onMouseOut={(e) => e.currentTarget.pause()}
                    onClick={()=>{setsingleViewer(!singleViewer)}}
                ></video>


                     
                
              


            </div>

                
              ))
              }
     
      
          
           
            


        




        </div>
                        <Separator className="mt-4" />
                                    <Footer></Footer>



        </div>:
         <div className="w-full h-screen overflow-hidden overscroll-none bg-zinc-900">
                <X className=" text-white bg-zinc-700 fixed w-10 h-10 mt-2 ml-2 hover:bg-slate-800 p-2  rounded-full" onClick={()=>{setsingleViewer(!singleViewer)}}/>







                <div className="flex flex-col items-center mt-20">
       <Carousel
      opts={{
        align: "start",
      }}
      orientation="vertical"
      className="w-full max-w-xs"
      plugins={[WheelGesturesPlugin()]}
      setApi={setApi}
    >
      <CarouselContent className="h-[600px] ">
        {videos.map((video, index) => (
          <CarouselItem  key={index} className="pt-1 ">
                       <div className="min-aspect-w-4 min-aspect-h-3 rounded-md bg-zinc-400">
                     <video 
                     ref={currentVideo}
                      className=" object-cover rounded-md hover:cursor-pointer"
                src={video}
                  loop={true} 
                 playsInline={true}
                 controls={true}
                 autoPlay={false}
                 
                    
                ></video>


                     
                
              



            </div>
           
          </CarouselItem>
        ))}
      </CarouselContent>
      <CarouselPrevious />
      <CarouselNext />
    </Carousel>
                    
          
            

                
                </div>

            </div>
                






        
    
    }
      



       
        
        </>
       
       
     );
}
 
export default Reels;