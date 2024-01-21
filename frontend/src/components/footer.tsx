import mascot from '../assets/mascot.png'

const Footer = () => {
    return ( 
             <div className='mt-8 flex flex-col items-center'>
                        <img className='w-28 h-28' src={mascot} alt="" />
                        <p className='text-sm font-montserrat text-zinc-400'>Built with love ❤️ by burdened bears</p>

      </div>
     );
}
 
export default Footer;