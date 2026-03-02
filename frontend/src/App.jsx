import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
    BarChart3,
    TrendingUp,
    ShieldCheck,
    Search,
    Activity,
    Zap,
    Globe,
    ChevronRight,
    LayoutDashboard,
    FileText,
    Cpu,
    Target,
    AlertTriangle,
    Info,
    Clock
} from 'lucide-react';

const App = () => {
    const [status, setStatus] = useState({ is_running: false });
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [selectedStock, setSelectedStock] = useState(null);
    const [activeTab, setActiveTab] = useState('portfolio');

    const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000/api";

    const fetchResults = async () => {
        try {
            const resp = await fetch(`${API_BASE}/results`);
            if (resp.ok) {
                const results = await resp.json();
                if (results && results.investments && results.investments.length > 0) {
                    setData(results);
                    setError(null);
                } else {
                    setError("No investment data found. Please run the analysis.");
                }
            } else {
                setError("Failed to fetch results from API. Is the backend running?");
            }
        } catch (err) {
            console.warn("Could not fetch latest results:", err);
            setError("Failed to connect to backend API. Ensure the backend is running.");
        } finally {
            setLoading(false);
        }
    };

    const checkStatus = async () => {
        try {
            const resp = await fetch(`${API_BASE}/status`);
            if (resp.ok) {
                const statusData = await resp.json();
                // If analysis just finished, trigger a data reload
                if (status.is_running && !statusData.is_running) {
                    console.log("Analysis finished, fetching new results...");
                    fetchResults();
                }
                setStatus(statusData);
            }
        } catch (err) {
            console.error("Status check failed:", err);
            setStatus({ is_running: false, message: "Backend unreachable" });
        }
    };

    const handleLaunchAnalysis = async () => {
        setLoading(true); // Show loading state while analysis starts
        setError(null); // Clear any previous errors
        try {
            const resp = await fetch(`${API_BASE}/run`, { method: 'POST' });
            if (resp.ok) {
                setStatus({ ...status, is_running: true, message: "Analysis started..." });
                console.log("Analysis launched successfully.");
            } else {
                const errorData = await resp.json();
                setError(`Failed to launch analysis: ${errorData.detail || resp.statusText}`);
                setStatus({ ...status, is_running: false });
            }
        } catch (err) {
            setError("System Launch Failed: " + err.message);
            setStatus({ ...status, is_running: false });
        }
    };

    useEffect(() => {
        fetchResults(); // Initial fetch
        checkStatus(); // Initial status check

        const interval = setInterval(() => {
            checkStatus();
        }, 5000); // Check status every 5 seconds

        return () => clearInterval(interval); // Cleanup on unmount
    }, [status.is_running]); // Re-run if analysis status changes

    const stocks = data?.investments || [];

    if (loading) {
        return (
            <div className="flex flex-col items-center justify-center min-h-screen bg-[#0e1117] text-gray-300">
                <motion.div
                    animate={{ rotate: 360 }}
                    transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
                    className="p-4 rounded-full border-t-2 border-indigo-500 mb-6"
                >
                    <Zap className="w-12 h-12 text-indigo-500 fill-indigo-500/20" />
                </motion.div>
                <p className="text-xl font-medium tracking-wide animate-pulse">Initializing StockAgent Intelligence...</p>
            </div>
        );
    }

    if (error) {
        return (
            <div className="flex flex-col items-center justify-center min-h-screen bg-[#0e1117] text-white p-6">
                <AlertTriangle className="w-16 h-16 text-red-500 mb-6" />
                <h2 className="text-2xl font-bold mb-2">Analysis Data Missing</h2>
                <p className="text-gray-400 max-w-md text-center mb-8">{error}</p>
                <div className="bg-gray-800/50 p-6 rounded-xl border border-gray-700/50 max-w-lg">
                    <h3 className="text-sm font-semibold uppercase tracking-wider text-gray-500 mb-3">Next Steps</h3>
                    <ol className="text-sm text-gray-300 space-y-2 list-decimal list-inside">
                        <li>Run <code>python -m stocksage.main run</code> if not already done</li>
                        <li>Verify files exist in <code>outputs/</code></li>
                        <li>Run <code>npm run copy-data</code> (or manual copy) to update frontend storage</li>
                    </ol>
                </div>
            </div>
        );
    }

    // Removed duplicate stocks declaration

    return (
        <div className="min-h-screen bg-[#0e1117] text-gray-200">
            {/* Navbar */}
            <nav className="sticky top-0 z-50 glass-card bg-[#0e1117]/80 border-b border-gray-800/80 px-6 py-4 flex items-center justify-between">
                <div className="flex items-center gap-3">
                    <div className="bg-indigo-500 p-2 rounded-lg glow-indigo">
                        <TrendingUp className="text-white w-6 h-6" />
                    </div>
                    <h1 className="text-2xl font-bold tracking-tight">
                        StockAgent <span className="text-indigo-500">Terminal</span>
                    </h1>
                </div>

                <div className="hidden md:flex items-center gap-8 text-sm font-medium">
                    <button
                        onClick={() => setActiveTab('portfolio')}
                        className={`flex items-center gap-2 transition-colors ${activeTab === 'portfolio' ? 'text-indigo-400' : 'text-gray-400 hover:text-white'}`}
                    >
                        <LayoutDashboard className="w-4 h-4" /> Dashboard
                    </button>
                    <button
                        className="flex items-center gap-2 text-gray-400 hover:text-white transition-colors"
                    >
                        <Search className="w-4 h-4" /> Market Explorer
                    </button>
                    <button
                        className="flex items-center gap-2 text-gray-400 hover:text-white transition-colors"
                    >
                        <Activity className="w-4 h-4" /> Live Feeds
                    </button>
                </div>

                <div className="flex items-center gap-6">
                    {/* Launch Button */}
                    <button
                        onClick={handleLaunchAnalysis}
                        disabled={status.is_running}
                        className={`px-4 py-2 rounded-xl text-xs font-bold uppercase tracking-widest transition-all ${status.is_running
                            ? 'bg-amber-500/10 text-amber-500 border border-amber-500/30 cursor-wait'
                            : 'bg-indigo-600 hover:bg-indigo-500 text-white shadow-lg shadow-indigo-500/20 active:scale-95'
                            }`}
                    >
                        {status.is_running ? (
                            <span className="flex items-center gap-2">
                                <motion.span animate={{ rotate: 360 }} transition={{ repeat: Infinity, duration: 1 }}><Cpu className="w-3 h-3" /></motion.span>
                                Analysis In Progress
                            </span>
                        ) : 'Launch System Analysis'}
                    </button>

                    <div className="hidden sm:block text-right">
                        <p className="text-xs text-gray-500 font-medium tracking-wider uppercase">Analyst Status</p>
                        <p className={`text-sm font-bold flex items-center gap-1.5 transition-all ${status.is_running ? 'text-amber-400' : 'text-green-400'}`}>
                            <span className="relative flex h-2 w-2">
                                <span className={`animate-ping absolute inline-flex h-full w-full rounded-full opacity-75 ${status.is_running ? 'bg-amber-400' : 'bg-green-400'}`}></span>
                                <span className={`relative inline-flex rounded-full h-2 w-2 ${status.is_running ? 'bg-amber-500' : 'bg-green-500'}`}></span>
                            </span>
                            {status.is_running ? 'System Computing' : 'AI Core Online'}
                        </p>
                    </div>
                </div>
            </nav>

            <main className="max-w-7xl mx-auto p-6 md:p-8">

                {/* Market Summary Header */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="glass-card p-6 rounded-2xl relative overflow-hidden group"
                    >
                        <div className="absolute top-0 right-0 p-8 opacity-5 group-hover:scale-110 transition-transform duration-500">
                            <Target className="w-24 h-24" />
                        </div>
                        <p className="text-gray-400 text-sm font-medium mb-1">Top Conviction</p>
                        <h3 className="text-3xl font-bold gradient-text">{stocks[0]?.ticker}</h3>
                        <p className="text-xs text-indigo-400/80 mt-2 flex items-center gap-1 font-semibold uppercase tracking-widest">
                            <Clock className="w-3 h-3" /> Updated Today
                        </p>
                    </motion.div>

                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.1 }}
                        className="glass-card p-6 rounded-2xl relative overflow-hidden group"
                    >
                        <div className="absolute top-0 right-0 p-8 opacity-5 group-hover:scale-110 transition-transform duration-500">
                            <BarChart3 className="w-24 h-24" />
                        </div>
                        <p className="text-gray-400 text-sm font-medium mb-1">Portfolio Sentiment</p>
                        <h3 className="text-3xl font-bold text-green-400">Bullish</h3>
                        <div className="w-full bg-gray-800 rounded-full h-1.5 mt-4">
                            <div className="bg-green-500 h-1.5 rounded-full w-[85%] shadow-[0_0_10px_rgba(34,197,94,0.3)]"></div>
                        </div>
                    </motion.div>

                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.2 }}
                        className="glass-card p-6 rounded-2xl relative overflow-hidden group"
                    >
                        <div className="absolute top-0 right-0 p-8 opacity-5 group-hover:scale-110 transition-transform duration-500">
                            <ShieldCheck className="w-24 h-24" />
                        </div>
                        <p className="text-gray-400 text-sm font-medium mb-1">Risk Profile</p>
                        <h3 className="text-3xl font-bold text-blue-400">Moderate</h3>
                        <p className="text-xs text-gray-500 mt-2 font-medium">Algorithmic Hedge Active</p>
                    </motion.div>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
                    {/* Stock List */}
                    <div className="lg:col-span-5 space-y-4">
                        <h2 className="text-sm font-bold uppercase tracking-[0.2em] text-gray-500 mb-4 px-2">Top Selections</h2>
                        {stocks.map((stock, index) => (
                            <motion.div
                                key={stock.ticker}
                                initial={{ opacity: 0, x: -20 }}
                                animate={{ opacity: 1, x: 0 }}
                                transition={{ delay: index * 0.1 }}
                                onClick={() => setSelectedStock(stock)}
                                className={`group cursor-pointer p-5 rounded-2xl transition-all duration-300 border-l-4 ${selectedStock?.ticker === stock.ticker
                                    ? 'bg-indigo-500/10 border-indigo-500 shadow-xl'
                                    : 'glass-card border-transparent hover:border-gray-600'
                                    }`}
                            >
                                <div className="flex items-center justify-between">
                                    <div className="flex items-center gap-4">
                                        <div className="w-12 h-12 rounded-xl bg-gray-800 flex items-center justify-center font-bold text-lg text-white border border-gray-700 shadow-inner group-hover:scale-110 transition-transform">
                                            {stock.ticker[0]}
                                        </div>
                                        <div>
                                            <h4 className="font-bold text-lg group-hover:text-indigo-400 transition-colors uppercase tracking-wide">{stock.ticker}</h4>
                                            <p className="text-xs text-gray-500 font-medium truncate max-w-[180px]">{stock.company_name}</p>
                                        </div>
                                    </div>
                                    <div className="text-right">
                                        <p className="text-sm font-bold text-indigo-400">TOP {index + 1}</p>
                                        <ChevronRight className={`w-5 h-5 transition-transform duration-300 ${selectedStock?.ticker === stock.ticker ? 'translate-x-1 text-indigo-400' : 'text-gray-700'}`} />
                                    </div>
                                </div>
                            </motion.div>
                        ))}
                    </div>

                    {/* Details View */}
                    <div className="lg:col-span-7">
                        <AnimatePresence mode="wait">
                            {selectedStock ? (
                                <motion.div
                                    key={selectedStock.ticker}
                                    initial={{ opacity: 0, scale: 0.98 }}
                                    animate={{ opacity: 1, scale: 1 }}
                                    exit={{ opacity: 0, scale: 0.98 }}
                                    className="glass-card rounded-[2rem] p-8 min-h-[600px] border border-gray-800/80 relative overflow-hidden"
                                >
                                    {/* Decorative Glow */}
                                    <div className="absolute -top-24 -right-24 w-64 h-64 bg-indigo-500/10 rounded-full blur-[100px]" />

                                    <div className="flex flex-wrap items-start justify-between gap-4 mb-8">
                                        <div>
                                            <div className="flex items-center gap-3 mb-2">
                                                <span className="px-3 py-1 bg-indigo-500/20 text-indigo-400 text-[10px] font-black uppercase tracking-[0.2em] rounded-full border border-indigo-500/30">
                                                    {selectedStock.details?.industry_classification?.sector || 'US EQUITIES'}
                                                </span>
                                                {selectedStock.details?.investment_thesis?.executive_summary?.recommendation && (
                                                    <span className="px-3 py-1 bg-green-500/20 text-green-400 text-[10px] font-black uppercase tracking-[0.2em] rounded-full border border-green-500/30">
                                                        {selectedStock.details.investment_thesis.executive_summary.recommendation}
                                                    </span>
                                                )}
                                            </div>
                                            <h2 className="text-4xl font-black tracking-tight text-white mb-1 uppercase">
                                                {selectedStock.company_name}
                                            </h2>
                                            <p className="text-gray-400 font-medium flex items-center gap-2">
                                                <Globe className="w-4 h-4 text-gray-500" />
                                                Global Market Component | NASDAQ listed
                                            </p>
                                        </div>

                                        <div className="bg-gray-800/80 p-5 rounded-[1.5rem] border border-gray-700 shadow-xl backdrop-blur-sm min-w-[120px] text-center">
                                            <p className="text-xs text-gray-500 font-bold uppercase tracking-widest mb-1">Conviction</p>
                                            <p className="text-2xl font-black text-white">
                                                {selectedStock.details?.investment_thesis?.executive_summary?.conviction_level || 'HIGH'}
                                            </p>
                                        </div>
                                    </div>

                                    <div className="space-y-10 relative z-10">
                                        <section>
                                            <h3 className="text-sm font-black text-gray-500 uppercase tracking-[0.3em] mb-4 flex items-center gap-2">
                                                <Zap className="w-4 h-4 text-indigo-500" /> Investment Thesis
                                            </h3>
                                            <p className="text-gray-300 leading-relaxed text-lg font-medium bg-indigo-500/5 p-6 rounded-2xl border border-indigo-500/10 italic">
                                                "{selectedStock.thesis}"
                                            </p>
                                        </section>

                                        {selectedStock.details && (
                                            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                                                <div>
                                                    <h3 className="text-sm font-black text-gray-500 uppercase tracking-[0.3em] mb-4 flex items-center gap-2">
                                                        <Target className="w-4 h-4 text-indigo-400" /> Strategy
                                                    </h3>
                                                    <ul className="space-y-3">
                                                        {selectedStock.details.investment_thesis.executive_summary.key_thesis_drivers.map((driver, i) => (
                                                            <li key={i} className="flex items-start gap-2.5 group">
                                                                <div className="mt-1.5 w-1.5 h-1.5 rounded-full bg-indigo-500 shadow-[0_0_8px_rgba(99,102,241,0.6)] group-hover:scale-125 transition-transform" />
                                                                <span className="text-sm text-gray-400 group-hover:text-gray-200 transition-colors">{driver}</span>
                                                            </li>
                                                        ))}
                                                    </ul>
                                                </div>

                                                <div>
                                                    <h3 className="text-sm font-black text-gray-500 uppercase tracking-[0.3em] mb-4 flex items-center gap-2">
                                                        <ShieldCheck className="w-4 h-4 text-blue-400" /> Risk Profile
                                                    </h3>
                                                    <div className="p-4 rounded-2xl bg-gray-800/40 border border-gray-700/50">
                                                        <p className="text-sm text-gray-400 leading-snug font-medium">
                                                            {selectedStock.details.investment_thesis.executive_summary.risk_assessment}
                                                        </p>
                                                    </div>
                                                </div>

                                                <div className="md:col-span-2">
                                                    <h3 className="text-sm font-black text-gray-500 uppercase tracking-[0.3em] mb-4 flex items-center gap-2">
                                                        <Cpu className="w-4 h-4 text-purple-400" /> Analysis Model
                                                    </h3>
                                                    <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
                                                        {[
                                                            { label: 'Valuation', val: 'Undervalued' },
                                                            { label: 'Growth', val: 'Accelerating' },
                                                            { label: 'Health', val: 'Superior' },
                                                            { label: 'Sentiment', val: 'Positive' }
                                                        ].map((item, i) => (
                                                            <div key={i} className="p-4 rounded-xl glass-card text-center hover:scale-105 transition-transform">
                                                                <p className="text-[10px] text-gray-500 font-black uppercase tracking-widest mb-1">{item.label}</p>
                                                                <p className="text-xs font-bold text-gray-100">{item.val}</p>
                                                            </div>
                                                        ))}
                                                    </div>
                                                </div>
                                            </div>
                                        )}
                                    </div>
                                </motion.div>
                            ) : (
                                <div className="glass-card rounded-[2rem] p-12 h-full flex flex-col items-center justify-center text-center border-dashed border-gray-800 border-2">
                                    <div className="w-24 h-24 bg-gray-800/50 rounded-full flex items-center justify-center mb-8 animate-bounce transition-all duration-1000">
                                        <Cpu className="w-10 h-10 text-gray-600" />
                                    </div>
                                    <h3 className="text-2xl font-bold text-white mb-3">Intelligence Readiness</h3>
                                    <p className="text-gray-500 max-w-sm font-medium leading-relaxed">
                                        Select a high-conviction security from the list to initialize the deep mechanical analysis and investment thesis engine.
                                    </p>
                                    <div className="mt-10 flex gap-4 text-xs font-black uppercase tracking-[0.2em] text-indigo-500">
                                        <span className="flex items-center gap-1"><Zap className="w-3 h-3" /> Real-time Data</span>
                                        <span className="text-gray-800">|</span>
                                        <span className="flex items-center gap-1"><ShieldCheck className="w-3 h-3" /> Secure Node</span>
                                    </div>
                                </div>
                            )}
                        </AnimatePresence>
                    </div>
                </div>
            </main>

            {/* Footer Info */}
            <footer className="max-w-7xl mx-auto px-6 py-12 mt-12 border-t border-gray-900 flex flex-wrap justify-between items-center gap-6">
                <div className="flex items-center gap-2">
                    <Info className="w-4 h-4 text-gray-600" />
                    <p className="text-xs text-gray-600 font-medium tracking-wide">
                        Generated by StockAgent Multi-Agent System. Strategic recommendations provided for information only.
                    </p>
                </div>
                <div className="flex gap-4">
                    {['Terminals', 'Protocols', 'Legal', 'System Status'].map((item) => (
                        <button key={item} className="text-[10px] uppercase font-black tracking-widest text-gray-700 hover:text-gray-400 transition-colors">
                            {item}
                        </button>
                    ))}
                </div>
            </footer>
        </div>
    );
};

export default App;
