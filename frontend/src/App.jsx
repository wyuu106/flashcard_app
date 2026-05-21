import { useEffect, useState } from "react"

function App() {
  const [isRegister, setIsRegister] = useState(false)
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")

  const [errorMessage, setErrorMessage] = useState("")
  const [successMessage, setSuccessMessage] = useState("")

  const [token, setToken] = useState(
    localStorage.getItem("token")
  )

  const [cards, setCards] = useState([])

  const [word, setWord] = useState("")
  const [meaning, setMeaning] = useState("")

  const [level, setLevel] = useState(1)
  const [exp, setExp] = useState(0)

  const [editingId, setEditingId] = useState(null)

  const [openId, setOpenId] = useState(null)

  const [quizQuestions, setQuizQuestions] = useState([])
  const [quizSessionId, setQuizSessionId] = useState(null)

  const [correctCount, setCorrectCount] = useState(0)
  const [currentIndex, setCurrentIndex] = useState(0)
  const [isAnswered, setIsAnswered] = useState(false)
  const [isCorrect, setIsCorrect] = useState(null)

  const [mode, setMode] = useState("list")

  useEffect(() => {
    if (token) {
      fetchCards()
      fetchUser()
    }
  }, [token])

  const fetchCards = () => {
    fetch("http://localhost:8000/cards", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }).then((res) => res.json())
      .then((data) => {
        setCards(data) 
      })
  }

  const fetchUser = () => {
    fetch("http://localhost:8000/users/me", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then((res) => res.json())
      .then((data) => {
        setLevel(data.level)
        setExp(data.exp)
      })
  }

  const login = async () => {
    const formData = new FormData()

    formData.append("username", username)
    formData.append("password", password)

    const res = await fetch(
      "http://localhost:8000/login",
      {
        method: "POST",
        body: formData,
      }
    )

    if (!res.ok) {
      setErrorMessage("ログイン失敗")
      return
    }

    setErrorMessage("")

    const data = await res.json()

    localStorage.setItem(
      "token",
      data.access_token
    )

    setToken(data.access_token)
  }

  const register = async () => {
    const res = await fetch(
      "http://localhost:8000/register",
      {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
        },

        body: JSON.stringify({
          name: username,
          password: password,
        }),
      }
    )

    if (!res.ok) {
      const data = await res.json()

      setErrorMessage(data.detail)

      return
    }

    setErrorMessage("")

    setSuccessMessage("登録成功")

    setUsername("")
    setPassword("")

    setIsRegister(false)
  }

  const logout = () => {
    localStorage.removeItem("token")

    setToken(null)
  }

  const deleteAccount = async () => {
    const ok = window.confirm(
      "本当にアカウントを削除しますか？"
    )

    if (!ok) {
      return
    }

    const res = await fetch(
      "http://localhost:8000/users/me",
      {
        method: "DELETE",

        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    )

    if (!res.ok) {
      alert("アカウント削除失敗")
      return
    }

    localStorage.removeItem("token")

    setToken(null)

    setCards([])
  }

  const addCard = () => {
    fetch("http://localhost:8000/cards", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
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

      headers: {
        Authorization: `Bearer ${token}`,
      },
    }).then(() => {
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
        Authorization: `Bearer ${token}`,
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

  const startQuiz = async () => {
    const res = await fetch(
      "http://localhost:8000/start",
      {
        method: "POST",

        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    )

    if (!res.ok) {
      alert("問題開始失敗")
      return
    }

    const data = await res.json()

    setQuizSessionId(data.session_id)
    setQuizQuestions(data.questions)
    setCurrentIndex(0)
    setIsAnswered(false)
    setIsCorrect(null)  
    setCorrectCount(0)
    setMode("quiz")
  }

  const currentCard =
    quizQuestions[currentIndex] || null

  const answerQuiz = async (choice) => {
    const res = await fetch(
      "http://localhost:8000/answer",
      {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },

        body: JSON.stringify({
          session_id: quizSessionId,
          card_id: currentCard.card_id,
          answer: choice,
        }),
      }
    )

    if (!res.ok) {
      alert("解答失敗")
      return
    }

    const data = await res.json()

    setCorrectCount(data.correct_count)
    setIsCorrect(data.is_correct)
    setIsAnswered(true)
  }

  const nextQuestion = async () => {
    setIsAnswered(false)

    setIsCorrect(null)

    if (currentIndex + 1 >= quizQuestions.length) {
      await endQuiz()
    } else {
      setCurrentIndex((prev) => prev + 1)
    }
  }

  const endQuiz = async () => {
    const res = await fetch(
      `http://localhost:8000/finish?session_id=${quizSessionId}`,
      {
        method: "POST",

        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    )

    if (!res.ok) {
      alert("終了失敗")
      return
    }

    const data = await res.json()

    fetchUser()

    alert(
      `${data.correct_count} / ${data.total_questions} 正解`
    )

    setMode("list")
    setQuizQuestions([])
    setCurrentIndex(0)
    setQuizSessionId(null)
    setCorrectCount(0)
    setIsAnswered(false)
    setIsCorrect(null)
  }

  if (!token) {
    return (
      <div>
        <h1>
          {isRegister ? "新規登録" : "ログイン"}
        </h1>

        {errorMessage && (
          <p>{errorMessage}</p>
        )}

        {successMessage && (
          <p>{successMessage}</p>
        )}

        <input
          type="text"
          placeholder="username"
          value={username}
          onChange={(e) =>
            setUsername(e.target.value)
          }
        />

        <input
          type="password"
          placeholder="password"
          value={password}
          onChange={(e) =>
            setPassword(e.target.value)
          }
        />

        {isRegister ? (
          <button onClick={register}>
            新規登録
          </button>
        ) : (
          <button onClick={login}>
            ログイン
          </button>
        )}

        <button
          onClick={() =>
            setIsRegister(!isRegister)
          }
        >
          {isRegister
            ? "ログインへ"
            : "新規登録へ"}
        </button>
      </div>
    )
  }

  return (
    <div>
      <div
        style={{
          position: "absolute",
          top: "10px",
          right: "10px",
          border: "1px solid black",
          padding: "10px",
        }}
      >
        <p>Lv. {level}</p>
        <p>Exp: {exp}</p>
      </div>

      {mode === "list" ? (
        <div>
          <h1>Flashcard App</h1>

          <button onClick={logout}>
            ログアウト
          </button>

          <button onClick={deleteAccount}>
            アカウント削除
          </button>

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
              変更
            </button>
          ) : (
            <button onClick={addCard}>
              追加
            </button>
          )}

          <button onClick={startQuiz}>
            問題を開始する
          </button>

          {cards.map((card) => (
            <div key={card.id} className="card">
              <h2>{card.word}</h2>

              {openId === card.id && (
                <p>{card.meaning}</p>
              )}

              <button onClick={() => deleteCard(card.id)}>
                削除
              </button>

              <button onClick={() => startEdit(card)}>
                編集
              </button>

              <button
                onClick={() =>
                  setOpenId(
                    openId === card.id ? null : card.id
                  )
                }
              >
                {openId === card.id ? "隠す" : "裏を見る"}
              </button>
            </div>
          ))}
        </div>
      ) : (
        <div>
          <h1>Quiz Mode</h1>

          <p>
            {currentIndex + 1} / {quizQuestions.length}
          </p>

          <p>
            正解数: {correctCount}
          </p>

          {currentCard && (
            <div className="card">
              <h2>{currentCard?.word}</h2>

              {currentCard?.choices.map((choice) => (
                <button
                  key={choice}
                  onClick={() => answerQuiz(choice)}
                  disabled={isAnswered}
                >
                  {choice}
                </button>
              ))}

              {isAnswered && currentCard && (
                <div>
                  <p>
                    {isCorrect ? "正解！" : "不正解"}
                  </p>

                  <p>
                    正解: {currentCard
                      ? cards.find(
                          (card) =>
                            card.id === currentCard.card_id
                        )?.meaning
                      : ""}
                  </p>

                  <button onClick={nextQuestion}>
                    次へ
                  </button>
                </div>
              )}

              <button onClick={endQuiz}>
                問題を終了する
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default App