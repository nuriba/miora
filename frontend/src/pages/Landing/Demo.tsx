import { motion } from 'framer-motion';
import { Play } from 'lucide-react';

const Demo = () => {
  return (
    <section id="demo" className="py-24 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
          className="text-center mb-12"
        >
          <h2 className="text-4xl md:text-5xl font-bold gradient-text mb-4">
            See Miora in Action
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Watch how easy it is to try on clothes virtually before you buy
          </p>
        </motion.div>
        
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          whileInView={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
          className="max-w-4xl mx-auto"
        >
          <div className="relative aspect-video bg-gradient-primary rounded-2xl overflow-hidden shadow-2xl">
            <div className="absolute inset-0 flex items-center justify-center">
              <button className="bg-white rounded-full p-6 shadow-lg hover:scale-110 transition-transform">
                <Play className="h-12 w-12 text-purple-600 ml-1" />
              </button>
            </div>
            <div className="absolute bottom-8 left-8 text-white">
              <p className="text-2xl font-bold">Interactive Demo</p>
              <p className="text-lg opacity-90">2 minutes</p>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
};

export default Demo; 