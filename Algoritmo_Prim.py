##________  ___  ___  ________  ___      ___ ________     
##|\   ____\|\  \|\  \|\   __  \|\  \    /  /|\   __  \    
##\ \  \___|\ \  \\\  \ \  \|\  \ \  \  /  / | \  \|\  \   
## \ \  \    \ \   __  \ \   __  \ \  \/  / / \ \   __  \  
##  \ \  \____\ \  \ \  \ \  \ \  \ \    / /   \ \  \ \  \ 
##   \ \_______\ \__\ \__\ \__\ \__\ \__/ /     \ \__\ \__\
##    \|_______|\|__|\|__|\|__|\|__|\|__|/       \|__|\|__|
##21310195 Meza Morales Salvador Emmanuel
import tkinter as tk
from tkinter import ttk, messagebox
import heapq
import networkx as nx
import matplotlib.pyplot as plt

class Graph:
    def __init__(self):
        self.edges = {}
        self.vertices = set()

    def add_edge(self, u, v, weight):
        if u not in self.edges:
            self.edges[u] = []
        if v not in self.edges:
            self.edges[v] = []
        self.edges[u].append((weight, v))
        self.edges[v].append((weight, u))
        self.vertices.add(u)
        self.vertices.add(v)

    def prim_min(self, start):
        min_heap = [(0, start)]
        mst = []
        visited = set()
        total_cost = 0
        steps = []
        while min_heap:
            weight, u = heapq.heappop(min_heap)
            if u in visited:
                continue
            visited.add(u)
            mst.append((weight, u))
            total_cost += weight
            steps.append((list(visited), list(min_heap)))
            for next_weight, v in self.edges[u]:
                if v not in visited:
                    heapq.heappush(min_heap, (next_weight, v))
        return mst, total_cost, steps

class PrimApp:
    def __init__(self, root):
        self.root = root
        self.graph = Graph()
        self.create_widgets()

    def create_widgets(self):
        self.root.title("Algoritmo de Prim - Árbol de Expansión Mínima")
        self.root.geometry("600x500")

        self.edge_frame = ttk.Frame(self.root)
        self.edge_frame.pack(pady=5)

        self.u_label = ttk.Label(self.edge_frame, text="Vértice U:")
        self.u_label.grid(row=0, column=0, padx=5, pady=5)
        self.u_entry = ttk.Entry(self.edge_frame)
        self.u_entry.grid(row=0, column=1, padx=5, pady=5)

        self.v_label = ttk.Label(self.edge_frame, text="Vértice V:")
        self.v_label.grid(row=1, column=0, padx=5, pady=5)
        self.v_entry = ttk.Entry(self.edge_frame)
        self.v_entry.grid(row=1, column=1, padx=5, pady=5)

        self.weight_label = ttk.Label(self.edge_frame, text="Peso:")
        self.weight_label.grid(row=2, column=0, padx=5, pady=5)
        self.weight_entry = ttk.Entry(self.edge_frame)
        self.weight_entry.grid(row=2, column=1, padx=5, pady=5)

        self.add_edge_button = ttk.Button(self.edge_frame, text="Agregar Arista", command=self.add_edge)
        self.add_edge_button.grid(row=3, column=0, columnspan=2, pady=5)

        self.show_edges_button = ttk.Button(self.root, text="Mostrar Aristas Guardadas", command=self.show_edges)
        self.show_edges_button.pack(pady=5)

        self.start_label = ttk.Label(self.root, text="Seleccione el vértice inicial:")
        self.start_label.pack(pady=5)
        self.start_entry = ttk.Entry(self.root)
        self.start_entry.pack(pady=5)

        self.solve_button = ttk.Button(self.root, text="Resolver", command=self.solve)
        self.solve_button.pack(pady=5)

        self.credits_button = ttk.Button(self.root, text="Créditos", command=self.show_credits)
        self.credits_button.pack(pady=5)

        self.result_text = tk.Text(self.root, height=10)
        self.result_text.pack(pady=5)

    def add_edge(self):
        u = self.u_entry.get()
        v = self.v_entry.get()
        try:
            weight = int(self.weight_entry.get())
        except ValueError:
            messagebox.showerror("Error", "El peso debe ser un número entero.")
            return
        self.graph.add_edge(u, v, weight)
        messagebox.showinfo("Información", f"Arista {u}-{v} con peso {weight} agregada.")

    def show_edges(self):
        edges_text = "Aristas guardadas:\n"
        for u in self.graph.edges:
            for weight, v in self.graph.edges[u]:
                edges_text += f"{u} - {v} con peso {weight}\n"
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, edges_text)

    def solve(self):
        start = self.start_entry.get()
        if start not in self.graph.vertices:
            messagebox.showerror("Error", "El vértice inicial no existe en el grafo.")
            return
        mst, total_cost, steps = self.graph.prim_min(start)
        
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"Árbol de Expansión con costo total: {total_cost}\n")
        self.result_text.insert(tk.END, "Aristas:\n")
        for weight, u in mst:
            self.result_text.insert(tk.END, f"{u} - peso: {weight}\n")

        self.show_graph(initial=True)
        self.show_steps(steps, "Prim Mínimo", start)

    def show_graph(self, initial=True, mst=None):
        G = nx.Graph()
        for u in self.graph.edges:
            for weight, v in self.graph.edges[u]:
                G.add_edge(u, v, weight=weight)

        pos = nx.spring_layout(G)
        plt.figure(figsize=(10, 7))
        if initial:
            title = "Grafo Inicial"
            nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10, font_weight='bold')
            labels = nx.get_edge_attributes(G, 'weight')
            nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        else:
            title = "Árbol de Expansión Mínima"
            mst_edges = [(u, v) for weight, u in mst]
            mst_graph = nx.Graph()
            for u in self.graph.edges:
                for weight, v in self.graph.edges[u]:
                    if (u, v) in mst_edges or (v, u) in mst_edges:
                        mst_graph.add_edge(u, v, weight=weight)
            nx.draw(mst_graph, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10, font_weight='bold')
            labels = nx.get_edge_attributes(mst_graph, 'weight')
            nx.draw_networkx_edge_labels(mst_graph, pos, edge_labels=labels)
            
        plt.title(title)
        plt.show()

    def show_steps(self, steps, algorithm, start):
        G = nx.Graph()
        for u in self.graph.edges:
            for weight, v in self.graph.edges[u]:
                G.add_edge(u, v, weight=weight)

        pos = nx.spring_layout(G)

        for i, (visited, heap) in enumerate(steps):
            plt.figure(figsize=(10, 7))
            nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10, font_weight='bold')
            labels = nx.get_edge_attributes(G, 'weight')
            nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
            
            nx.draw_networkx_nodes(G, pos, nodelist=visited, node_color='green')
            plt.title(f"Paso {i + 1} - Algoritmo: {algorithm} - Vértice inicial: {start}")
            plt.show()

    def show_credits(self):
        credits = tk.Toplevel(self.root)
        credits.title("Créditos")
        credits.geometry("400x200")
        tk.Label(credits, text="Salvador Emmanuel Meza Morales", font=("Helvetica", 16, "bold")).pack(pady=20)
        tk.Label(credits, text="21310195", font=("Helvetica", 14)).pack(pady=10)
        tk.Button(credits, text="Cerrar", command=credits.destroy).pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = PrimApp(root)
    root.mainloop()
