from flask import Flask, render_template, request
app = Flask(__name__)

import pandas as pd
import geopandas as gpd
import os
import matplotlib.pyplot as plt
import contextily as ctx

quartieri = gpd.read_file("Quartieri/NIL_WM.dbf")
fontane = gpd.read_file("Fontanelle/Fontanelle_OSM_ODbL.dbf")

@app.route("/")
def home():
    lista_quartieri = list(set(quartieri["NIL"]))
    lista_quartieri.sort()
    return render_template("home.html", lista = lista_quartieri)

@app.route("/es1", methods = ["GET"])
def es1():
    q = request.args.get("quartiere")
    quartiere_selezionato = quartieri[quartieri["NIL"].str.contains(q.upper())].to_crs(3857)
    ax = quartiere_selezionato.plot(figsize = (12, 6), facecolor = "none", edgecolor = "k", linewidth = 2)
    ctx.add_basemap(ax)

    dir = "static/images"
    file_name = "es1.png"
    save_path = os.path.join(dir, file_name)
    plt.savefig(save_path, dpi = 150)
    return render_template("es1.html")

@app.route("/es2")
def es2():
    ax = fontane.to_crs(3857).plot(figsize = (12, 6), markersize = 15, color = "red")
    ctx.add_basemap(ax)

    dir = "static/images"
    file_name = "es2.png"
    save_path = os.path.join(dir, file_name)
    plt.savefig(save_path, dpi = 150)
    return render_template("es2.html")

@app.route("/es3")
def es3():
    quartieri_fontane = quartieri[quartieri.intersects(fontane.unary_union)].to_crs(3857)
    ax = quartieri_fontane.plot(figsize = (15, 8), edgecolor = "k", facecolor = "none")
    fontane.to_crs(3857).plot(ax = ax, markersize = 13, color = "red")
    ctx.add_basemap(ax)

    dir = "static/images"
    file_name = "es3.png"
    save_path = os.path.join(dir, file_name)
    plt.savefig(save_path, dpi = 150)
    return render_template("es3.html")

@app.route("/es4")
def es4():
    quartieri_fontane = quartieri[quartieri.intersects(fontane.unary_union)].to_crs(3857)
    joined = gpd.sjoin(fontane.to_crs(3857), quartieri_fontane, how = "left")
    fontane_per_quartiere = joined.groupby("NIL").count()[["Licenza"]].sort_values(by = "Licenza", ascending = False).reset_index()
    finale = quartieri_fontane.merge(fontane_per_quartiere, on = "NIL")
    ax = finale.plot(figsize = (15, 9), column = "Licenza", legend = True, alpha = 0.6)
    ctx.add_basemap(ax)

    dir = "static/images"
    file_name = "es4.png"
    save_path = os.path.join(dir, file_name)
    plt.savefig(save_path, dpi = 150)
    return render_template("es4.html")

@app.route("/es5")
def es5():
    quartieri_fontane = quartieri[quartieri.intersects(fontane.unary_union)].to_crs(3857)
    joined = gpd.sjoin(fontane.to_crs(3857), quartieri_fontane, how = "left")
    fontane_per_quartiere = joined.groupby("NIL").count()[["Licenza"]].sort_values(by = "Licenza", ascending = False).reset_index()
    dati = fontane_per_quartiere["Licenza"]
    stringhe = fontane_per_quartiere["NIL"]
    plt.figure(figsize=(16, 8))
    plt.pie(dati, labels=stringhe, autopct='%1.1f%%')

    dir = "static/images"
    file_name = "es5.png"
    save_path = os.path.join(dir, file_name)
    plt.savefig(save_path, dpi = 150)
    return render_template("es5.html")


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)