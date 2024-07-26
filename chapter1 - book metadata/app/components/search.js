import { useReducer, useRef, useState } from "react"


export default function Search({queryUpdater}) {

    const qRef = useRef()
    function updateQuery() {
        queryUpdater(qRef.current.value)
    }

    return (
         <div className="flex justify-center mt-4">
            <input
                type="search"
                placeholder="Search..."
                className="w-full p-4 pl-12 text-gray-700 text-lg border-b-2 border-gray-200 focus:outline-none focus:border-indigo-500"
                ref={qRef}
            />
            <button
                type="submit"
                className="bg-indigo-500 hover:bg-indigo-600 text-white font-bold py-2 px-4 rounded"
                onClick={updateQuery}
            >
                Search
            </button>
      </div>   
    )
}