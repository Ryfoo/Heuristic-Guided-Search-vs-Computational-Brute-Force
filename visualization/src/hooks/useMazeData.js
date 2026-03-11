import { useState, useEffect } from 'react'

export function useMazeData(url) {
    const [data,    setData]    = useState(null)
    const [loading, setLoading] = useState(true)
    const [error,   setError]   = useState(null)

    useEffect(() => {
        fetch(url)
            .then(res => {
                if (!res.ok) throw new Error(`Failed to load ${url}`)
                return res.json()
            })
            .then(json => {
                setData(json)
                setLoading(false)
            })
            .catch(err => {
                setError(err.message)
                setLoading(false)
            })
    }, [url])

    return { data, loading, error }
}
