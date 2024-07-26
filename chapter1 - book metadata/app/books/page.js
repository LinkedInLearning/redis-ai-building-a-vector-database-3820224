'use client'
import  { useState, useEffect  } from 'react';
import Search from '../components/search';

export default function BookList() {
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [query, setQuery] = useState("")

  useEffect(() => {
    fetch('/books/api')
      .then(response => response.json())
      .then( data => data.filter(bookData => {
        return bookData.title.indexOf(query) != -1
      }))
      .then(data => {
        setBooks(data);
        setLoading(false);
      })
      .catch(error => {
        console.error(error);
        setLoading(false);
      });
  }, [query]);

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div className="grid grid-cols-1 gap-4">
    <Search queryUpdater={setQuery}/>
      {books.map(book => (
        <div key={book.id} className="bg-white shadow-md p-4 rounded">
          <h2 className="text-lg font-bold">{book.title}</h2>
          <p className="text-gray-700">{book.author}</p>
          <p className="text-gray-700">{book.releaseDate}</p>
        </div>
      ))}
    </div>
  );
}