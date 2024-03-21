const QueryInput = () => {
  return (
    <div className="w-screen flex items-center justify-center">
      <input
        type="text"
        className="mt-10 rounded-l text-center border-b-1 focus:outline-none w-3/6"
        placeholder="Query Sequence(s)"
      />
    </div>
  )
}

export default QueryInput
