import { motion } from 'framer-motion';

const steps = [
  {
    number: '01',
    title: 'Create Your Avatar',
    description: 'Take a selfie or enter your measurements to create a hyper-realistic 3D avatar that matches your body perfectly.',
    icon: '🤳',
  },
  {
    number: '02',
    title: 'Import Clothes',
    description: 'Add clothes from any website, upload photos, or browse our partner brands\' latest collections.',
    icon: '👕',
  },
  {
    number: '03',
    title: 'Virtual Try-On',
    description: 'See how clothes look, fit, and move on your avatar with realistic physics simulation.',
    icon: '✨',
  },
  {
    number: '04',
    title: 'Shop & Share',
    description: 'Get size recommendations, purchase with confidence, and share your looks with friends.',
    icon: '🛍️',
  },
];

const HowItWorks = () => {
  return (
    <section id="how-it-works" className="py-24 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl md:text-5xl font-bold gradient-text mb-4">
            How It Works
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Get started with Miora in four simple steps
          </p>
        </motion.div>
        
        <div className="grid md:grid-cols-4 gap-8">
          {steps.map((step, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              viewport={{ once: true }}
              className="text-center"
            >
              <div className="relative">
                <div className="w-20 h-20 bg-gradient-primary rounded-full flex items-center justify-center mx-auto mb-6">
                  <span className="text-white text-2xl font-bold">{step.number}</span>
                </div>
                {index < steps.length - 1 && (
                  <div className="hidden md:block absolute top-10 left-full w-full h-0.5 bg-gradient-to-r from-purple-500 to-transparent" />
                )}
              </div>
              <div className="text-4xl mb-4">{step.icon}</div>
              <h3 className="text-xl font-semibold mb-2">{step.title}</h3>
              <p className="text-gray-600">{step.description}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default HowItWorks; 