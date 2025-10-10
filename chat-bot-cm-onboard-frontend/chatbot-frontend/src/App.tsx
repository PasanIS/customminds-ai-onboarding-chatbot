import ChatWidget from "./components/ChatPopup";

function App() {
  return (
    <div className="App flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <h1 className="text-4xl font-bold text-blue-600 text-center mb-6 drop-shadow-lg">
        Welcome to My Website
      </h1>
      <ChatWidget />
    </div>
  );
}

export default App;
