import matplotlib.pyplot as plt


def drawModa(data, path) -> None:

    plt_name = 'Moda.png'

    
    x = range(len(data))
    max_intx = max(data)
    max_inty = data.index(max_intx)
    plt.plot(x, data)  
    plt.scatter([max_inty], [max_intx], color='red')
    plt.vlines(max_inty, 0, max_intx, linestyles='dashed', colors='gray')

    plt.xlim([0, x[-1]]) 
    plt.ylim([0, max_intx + 1])
    plt.title("Частота пересечений подинтервалов с интервалами выборки")  
    plt.xlabel("Индекс") 
    plt.ylabel("Частота")  
    plt.savefig(path+plt_name, dpi=300)
 

    
def drawMultyModa(freq, segments_indices, max_freqs, path):
    plt_name = 'multyModa.png'

    # Визуализация
    plt.figure(figsize=(10, 5))

    plt.plot(freq, color='lightgrey', zorder=1)

    colors = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black']
    for i, (start, end) in enumerate(segments_indices):
        
        plt.fill_between(range(start, end+1), freq[start:end+1], color=colors[i % len(colors)], alpha=0.5, zorder=2)
        
        
        max_index = max_freqs[i]  
        max_val = freq[max_index]  
        plt.scatter(max_index, max_val, color='black', zorder=3)  

    plt.title('Мультимода')
    plt.xlabel('Индекс')
    plt.ylabel('Значение')
    plt.grid(True)
    plt.savefig(path+plt_name, dpi=300)



    