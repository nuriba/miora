import { Link } from 'react-router-dom';
import Hero from './Hero';
import Features from './Features';
import HowItWorks from './HowItWorks';
import Demo from './Demo';
import CTA from './CTA';
import Footer from '../../components/layout/Footer';

const Landing = () => {
  return (
    <div className="min-h-screen">
      {/* Navigation */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-white/90 backdrop-blur-md border-b border-gray-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-20">
            <Link to="/" className="text-3xl font-bold gradient-text">
              Miora
            </Link>
            
            <div className="hidden md:flex items-center space-x-8">
              <a href="#features" className="text-gray-700 hover:text-purple-600 transition">
                Features
              </a>
              <a href="#how-it-works" className="text-gray-700 hover:text-purple-600 transition">
                How It Works
              </a>
              <a href="#demo" className="text-gray-700 hover:text-purple-600 transition">
                Demo
              </a>
              <a href="#contact" className="text-gray-700 hover:text-purple-600 transition">
                Contact
              </a>
            </div>
            
            <div className="flex items-center space-x-4">
              <Link to="/login" className="btn btn-secondary">
                Sign In
              </Link>
              <Link to="/register" className="btn btn-primary">
                Get Started
              </Link>
            </div>
          </div>
        </div>
      </nav>
      
      {/* Sections */}
      <Hero />
      <Features />
      <HowItWorks />
      <Demo />
      <CTA />
      <Footer />
    </div>
  );
};

export default Landing;