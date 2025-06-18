const LoadingSpinner = () => {
    return (
      <div className="absolute inset-0 flex items-center justify-center bg-white/80 backdrop-blur-sm">
        <div className="relative">
          <div className="w-16 h-16 border-4 border-purple-200 rounded-full animate-spin border-t-purple-600" />
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="w-8 h-8 bg-gradient-primary rounded-full animate-pulse" />
          </div>
        </div>
      </div>
    );
  };
  
  export default LoadingSpinner;