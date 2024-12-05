import { useEffect, useState } from "react";
import axios from "axios";
import Latex from "react-latex-next";
import 'katex/dist/katex.min.css';

const API_BASE_URL = "http://localhost:8000";

function App() {
  const [topics, setTopics] = useState([]);
  const [selectedTopic, setSelectedTopic] = useState(null);
  const [problem, setProblem] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchTopics = async () => {
      try {
        const response = await axios.get(`${API_BASE_URL}/topic`);
        setTopics(response.data);
      } catch (error) {
        console.error("Error fetching topics:", error);
      }
    };
    fetchTopics();
  }, []);

  // Generate problem for selected topic
  const generateProblem = async () => {
    if (selectedTopic === null) return;
    setLoading(true);
    try {
      const response = await axios.get(
        `${API_BASE_URL}/problem/${selectedTopic}`
      );
      console.log(response.data);
      setProblem(response.data);
    } catch (error) {
      console.error("Error generating problem:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center py-10">
      <h1 className="text-2xl font-bold mb-5">Mathellm: Math Problem Generator</h1>

      {/* Topic Selection */}
      <div className="w-full max-w-xl">
        <label htmlFor="topic-select" className="block text-sm font-medium text-gray-700 mb-2">
          Select a Topic:
        </label>
        <select
          id="topic-select"
          className="w-full px-3 py-2 border rounded shadow-sm focus:outline-none focus:ring focus:ring-blue-300"
          value={selectedTopic === null ? "-1" : selectedTopic}
          onChange={(e) => setSelectedTopic(Number(e.target.value))}
        >
          <option value="-1" disabled>
            -- Choose a topic --
          </option>
          {topics.map((topic) => (
            <option key={topic.id} value={topic.id}>
              {topic.name}
            </option>
          ))}
        </select>
      </div>

      {/* Generate Problem Button */}
      <button
        onClick={generateProblem}
        disabled={selectedTopic === null || loading}
        className="mt-5 px-4 py-2 bg-blue-500 text-white rounded shadow hover:bg-blue-600 disabled:opacity-50"
      >
        {loading ? "Generating..." : "Generate Problem"}
      </button>

      {/* Problem Display */}
      {problem && (
        <div className="w-full max-w-xl mt-8 bg-white p-5 shadow rounded">
          <h2 className="text-lg font-bold mb-3">{problem.name}</h2>
          <p className="text-gray-700"> <strong>Description:</strong> {problem.description} </p>
          <p className="text-gray-700"> <strong>Level:</strong> {problem.level} </p>
          <p className="text-gray-700"> <strong>Difficulty:</strong> {problem.difficulty} </p>
          <p className="text-gray-700"> <strong>Tags:</strong> {problem.tags.join(", ")} </p>
          <p className="text-gray-700 mt-3"> <strong>Content:</strong> </p>
          <p className="bg-gray-50 p-3 rounded">
            <Latex>{problem.content}</Latex>
          </p>
          {problem.solution && (
            <div>
              <p className="text-gray-700 mt-3"> <strong>Solution:</strong> </p>
              {problem.solution.map((sol, index) => (
                <p className="bg-gray-50 p-3 rounded" key={index}>
                  <Latex>{`$$${sol}$$`}</Latex>
                </p>
              ))}
            </div>
          )}
          {problem.answer && (
            <div>
              {Object.keys(problem.answer)
                .filter((key) => problem.answer[key] !== null)
                .map((key, index) => (
                  <div key={index}>
                    <p className="text-gray-700 mt-3"> <strong>{`Answer in ${key}:`}</strong> </p>
                    <p className="bg-gray-50 p-3 rounded" key={index}>
                      <Latex>{problem.answer[key]}</Latex>
                    </p>
                  </div>
                ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
