import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { Play } from 'lucide-react';

const Hero = () => {
  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
      {/* Background */}
      <div className="absolute inset-0 bg-gradient-to-br from-[#7f5af0] to-[#764ba2] opacity-100 z-0" />
      <div className="absolute inset-0 bg-[url('/pattern.svg')] opacity-10 z-0" />

      {/* Content */}
      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          <h1 className="text-5xl md:text-7xl font-bold text-white mb-6">
            Try Before You Buy
          </h1>
          <p className="text-xl md:text-2xl text-white/90 mb-12 max-w-3xl mx-auto">
            Create your perfect 3D avatar and virtually try on any outfit with 
            hyper-realistic simulation. Shop with confidence, reduce returns, 
            and discover your perfect style.
          </p>

          <div className="flex flex-col sm:flex-row gap-10 justify-center items-center">
          <Link to="/register" className="btn btn-primary bg-white text-white hover:bg-gray-100">
              Start Your Virtual Wardrobe
            </Link>
          <Link to="/demo" className="px-6 py-3 rounded-full border-2 border-white text-white hover:bg-white/10 flex items-center gap-2 transition">
            <Play className="h-5 w-5" />
            Watch Demo
          </Link>
          </div>
        </motion.div>
      </div>

      {/* Scroll indicator */}
      <motion.div
        className="absolute bottom-6 left-1/2 transform -translate-x-1/2 cursor-pointer z-10"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.2, duration: 0.5 }}
        onClick={() => {
          const nextSection = document.querySelector('#features');
          nextSection?.scrollIntoView({ behavior: 'smooth' });
        }}
      >
        <div className="w-6 h-10 border-2 border-white rounded-full flex justify-center items-start bg-white/10 backdrop-blur-sm hover:bg-white/20 transition">
          <motion.div 
            className="w-1 h-3 bg-white rounded-full mt-2"
            animate={{ y: [0, 6, 0] }}
            transition={{ repeat: Infinity, duration: 1.5, ease: "easeInOut" }}
          />
        </div>
      </motion.div>
    </section>
  );
};

export default Hero;