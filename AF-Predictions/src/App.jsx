import QueryInput from "./components/QueryInput";

function App() {
  return (
    <div className="flex flex-col items-center h-screen w-screen bg-black">
      <header className="text-white text-2xl mt-3">AF Predictions</header>
      <QueryInput />
    </div>
  );
}

export default App;
