import { useEffect, useState } from "react"

function App() {
  const [cards, setCards] = useState([])
  const [word, setWord] = useState("")
  const [meaning, setMeaning] = useState("")
  const [editingId, setEditingId] = useState(null)
  const [showMeaning, setShowMeaning] = useState(false)

  useEffect(() => {
    fetchCards()
  }, [])

  const fetchCards = () => {
    fetch("http://localhost:8000/cards")
      .then((res) => res.json())
      .then((data) => {
        setCards(data)
      })
  }

  const addCard = () => {
    fetch("http://localhost:8000/cards", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        word: word,
        meaning: meaning,
      }),
    }).then(() => {
      fetchCards()

      setWord("")
      setMeaning("")
    })
  }

  const deleteCard = (id) => {
    fetch(`http://localhost:8000/cards/${id}`, {
      method: "DELETE",
    })
      .then((res) => res.json())
      .then(() => {
        fetchCards()
      })
  }

  const startEdit = (card) => {
    setEditingId(card.id)
    setWord(card.word)
    setMeaning(card.meaning)
  }

  const updateCard = () => {
    fetch(`http://localhost:8000/cards/${editingId}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        word: word,
        meaning: meaning,
      }),
    }).then(() => {
      fetchCards()

      setEditingId(null)
      setWord("")
      setMeaning("")
    })
  }

  return (
    <div>
      <h1>Flashcard App</h1>

      <input
        type="text"
        placeholder="word"
        value={word}
        onChange={(e) => setWord(e.target.value)}
      />

      <input
        type="text"
        placeholder="meaning"
        value={meaning}
        onChange={(e) => setMeaning(e.target.value)}
      />

      {editingId ? (
        <button onClick={updateCard}>
          Update
        </button>
      ) : (
        <button onClick={addCard}>
          Add
        </button>
      )}

      {cards.map((card) => (
        <div key={card.id} className="card">
          <h2>{card.word}</h2>
          {showMeaning && <p>{card.meaning}</p>}

          <button onClick={() => deleteCard(card.id)}>
            Delete
          </button>

         <button onClick={() => startEdit(card)}>
            Edit
         </button>

         <button onClick={() => setShowMeaning(!showMeaning)}>
            {showMeaning ? "Hide" : "Show"}
         </button>
         
        </div>
      ))}
    </div>
  )
}

export default App