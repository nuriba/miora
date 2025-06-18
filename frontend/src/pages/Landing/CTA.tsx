import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { ArrowRight } from 'lucide-react';

const CTA = () => {
  return (
    <section id="contact" className="py-24 bg-gradient-primary">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
        >
          <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
            Ready to Transform Your Shopping?
          </h2>
          <p className="text-xl text-white/90 mb-8 max-w-3xl mx-auto">
            Join thousands of users who've discovered their perfect style with Miora.
            Start your free trial today - no credit card required.
          </p>
          <Link
            to="/register"
            className="btn bg-white text-purple-600 hover:bg-gray-100 inline-flex items-center"
          >
            Start Free Today
            <ArrowRight className="ml-2 h-5 w-5" />
          </Link>
          <p className="mt-4 text-white/70">
            ✓ Free forever for up to 10 garments ✓ No credit card required
          </p>
        </motion.div>
      </div>
    </section>
  );
};

export default CTA; 