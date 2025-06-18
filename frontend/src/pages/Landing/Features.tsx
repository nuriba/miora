import { motion } from 'framer-motion';
import { Target, Shield, Sparkles, Users, Smartphone, Globe } from 'lucide-react';

const features = [
  {
    icon: Target,
    title: 'Perfect Fit Guarantee',
    description: 'Our AI analyzes your body measurements and recommends the perfect size for every garment, reducing returns by up to 80%.',
  },
  {
    icon: Shield,
    title: 'Privacy First',
    description: 'Your body data stays on your device. We use advanced encryption to protect your privacy while providing personalized experiences.',
  },
  {
    icon: Sparkles,
    title: 'Realistic Simulation',
    description: 'Experience hyper-realistic cloth physics that shows exactly how garments will drape, stretch, and move on your body.',
  },
  {
    icon: Users,
    title: 'Social Shopping',
    description: 'Share your outfits, get feedback from friends, and discover trending styles in our vibrant fashion community.',
  },
  {
    icon: Smartphone,
    title: 'Cross-Platform',
    description: 'Seamlessly switch between web and mobile. Your avatar and wardrobe sync across all devices for shopping anywhere.',
  },
  {
    icon: Globe,
    title: 'Universal Compatibility',
    description: 'Works with any online store. Import clothes from any website or upload your own photos to try them on virtually.',
  },
];

const Features = () => {
  return (
    <section id="features" className="py-24 bg-gradient-to-b from-gray-50 to-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl md:text-5xl font-bold gradient-text mb-4">
            Why Choose Miora?
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Experience the future of online shopping with our cutting-edge virtual try-on technology
          </p>
        </motion.div>
        
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              viewport={{ once: true }}
              className="card hover:shadow-xl"
            >
              <feature.icon className="h-12 w-12 text-purple-600 mb-4" />
              <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
              <p className="text-gray-600">{feature.description}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Features;