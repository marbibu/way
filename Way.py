from __future__ import generators
class priorityDictionary(dict):
	def __init__(self):
		#Initialize priorityDictionary by creating binary heap of pairs (value,key).
            #Note that changing or removing a dict entry will not remove the old pair from the heap
            #until it is found by smallest() or until the heap is rebuilt.
		self.__heap = []
		dict.__init__(self)
	def smallest(self):
		'''Find smallest item after removing deleted items from front of heap.'''
		if len(self) == 0:
			raise IndexError, "smallest of empty priorityDictionary"
		heap = self.__heap
		while heap[0][1] not in self or self[heap[0][1]] != heap[0][0]:
			lastItem = heap.pop()
			insertionPoint = 0
			while 1:
				smallChild = 2*insertionPoint+1
				if smallChild+1 < len(heap) and heap[smallChild] > heap[smallChild+1] :
					smallChild += 1
				if smallChild >= len(heap) or lastItem <= heap[smallChild]:
					heap[insertionPoint] = lastItem
					break
				heap[insertionPoint] = heap[smallChild]
				insertionPoint = smallChild
		return heap[0][1]
	
	def __iter__(self):
		'''Create destructive sorted iterator of priorityDictionary.'''
		def iterfn():
			while len(self) > 0:
				x = self.smallest()
				yield x
				del self[x]
		return iterfn()
	
	def __setitem__(self,key,val):
		#Change value stored in dictionary and add corresponding pair to heap.
            #Rebuilds the heap if the number of deleted items gets large, to avoid memory leakage.
		dict.__setitem__(self,key,val)
		heap = self.__heap
		if len(heap) > 2 * len(self):
			self.__heap = [(v,k) for k,v in self.iteritems()]
			self.__heap.sort()  # builtin sort probably faster than O(n)-time heapify
		else:
			newPair = (val,key)
			insertionPoint = len(heap)
			heap.append(None)
			while insertionPoint > 0 and newPair < heap[(insertionPoint-1)//2]:
				heap[insertionPoint] = heap[(insertionPoint-1)//2]
				insertionPoint = (insertionPoint-1)//2
			heap[insertionPoint] = newPair
	
	def setdefault(self,key,val):
		'''Reimplement setdefault to pass through our customized __setitem__.'''
		if key not in self:
			self[key] = val
		return self[key]
class Sender:
      #Klasa, ktora rozsyla info do odbiorcow
      def __init__(s):
            #Dane:
            s.__listeners=[]
      def addListener(s,listener):#Dodaje sluchacza
            s.__listeners.append(listener)
      def delListener(s,listener):#Usuwa sluchacza
            s.__listeners.remove(listener)
      def sendSignal(s):#Wysyla sygnal
            for i in s.__listeners:
                  i.receiveSignal(s)
      def getName(s):#Zwraca nazwe nadawcy
            return s.__class__.__name__
class Listener:
      #Klasa, ktora umozliwia odbieranie sygnalow od nadawcy
      def __init__(s):
            #Dane:
            pass
      def receiveSignal(s,sender):
            print "Nie zaimplementowano odbierania sygnalow"
      def listen2(s,sender):#Rozpoczyna nasluchiwanie wskazanego nadawcy
            sender.addListener(s)

class Pool(Sender):
      #Klasa, ktora tworzy obiekt pola
      def __init__(s,x,y,weight):
            #Dane:
            Sender.__init__(s)
            s.__x,s.__y=x,y
            s.__weight=weight
            s.__neighbours=[None,None,None,None]#top,bottom,left,right
      def __str__(s):
            return "(%s,%s)"%(s.__x,s.__y)
      def getXY(s):#Zwraca wspolrzedne punktu
            return s.__x,s.__y
      def setWeight(s,weight):#Ustawia wage pola
            s.__weight=weight
            s.sendSignal()
      def getWeight(s):#Zwraca wage pola
            return s.__weight
      def setLeft(s,pool):#Ustawia pole sasiadujace od lewej strony
            s.__neighbours[2]=pool
      def setRight(s,pool):#Ustawia pole sasiadujace od prawej strony
            s.__neighbours[3]=pool
      def setTop(s,pool):#Ustawia pole sasiadujace od gornej strony
            s.__neighbours[0]=pool
      def setBottom(s,pool):#Ustawia pole sasiadujace od dolnej strony
            s.__neighbours[1]=pool
      def getNeighbours(s):#Zwraca liste sasiadow
            return s.__neighbours
      def showNeighbours(s):#Wyswietla liste punktow
            for i in s.__neighbours:
                  print i
from copy import deepcopy
class Board(Sender):
      #Klasa, ktora tworzy plansze
      def __init__(s,m,n):
            #Dane:
            s.__m,s.__n=m,n
            Sender.__init__(s)
            s.__poolSL={}
            #Definicje:
            s.__genPools(m,n)
            s.__genNeighbours()
      def __genPools(s,m,n):#Generuje punkty
            for i in range(m):
                  for j in range(n):
                        s.__poolSL["%s,%s"%(i,j)]=Pool(i,j,30)
      def getPoolWithXY(s,x,y):#Zwraca id pola o wskazanych wspolrzednych
            return s.__poolSL["%s,%s"%(x,y)]
      def getMN(s):#Zwraca rozmiar pola
            return s.__m,s.__n
      def __genNeighbours(s):
            for i in range(s.__m):
                  for j in range(s.__n):
                        pool=s.getPoolWithXY(i,j)
                        pool.setTop(s.__hasPool(i,j-1))
                        pool.setBottom(s.__hasPool(i,j+1))
                        pool.setLeft(s.__hasPool(i-1,j))
                        pool.setRight(s.__hasPool(i+1,j))
                        
      def __hasPool(s,x,y):#Sprawdza czy istnieje pole, jezeli tak to je zwraca
            if s.__poolSL.has_key("%s,%s"%(x,y)):
                  return s.__poolSL["%s,%s"%(x,y)]
            else:
                  return None
      def __dijkstra(s,start,end):
            G={}
            for i in s.__poolSL.keys():
                  sl={}
                  for j in s.__poolSL[i].getNeighbours():
                        if j==None:
                              pass
                        else:
                              sl[j]=j.getWeight()
                  G[s.__poolSL[i]]=sl
            D = {}	# dictionary of final distances
            P = {}	# dictionary of predecessors
            Q = priorityDictionary()   # est.dist. of non-final vert.
            Q[start] = 0
            
            for v in Q:
                  D[v] = Q[v]
                  if v == end: break
                  
                  for w in G[v]:
                        vwLength = D[v] + G[v][w]
                        if w in D:
                              if vwLength < D[w]:
                                    raise ValueError, "Dijkstra: found better path to already-final vertex"
                        elif w not in Q or vwLength < Q[w]:
                              Q[w] = vwLength
                              P[w] = v
            return (D,P)
                        
      def shortestPath(s,start,end):
            D,P = s.__dijkstra(start,end)
            path = []
            while 1:
                  path.append(end)
                  if end == start: break
                  end = P[end]
            path.reverse()
            return path
      def getPools(s):#Zwraca liste pol
            return s.__poolSL.values()

class Way:
      #Klasa, ktora tworzy obiekt drogi
      def __init__(s,start,meta):
            #Dane:
            
            s.__start=start
            s.__meta=meta
            print "start",start
            #s.__current=Pointer(s,start,None,0)
      def getMeta(s):#Zwraca id pola mety
            return s.__meta
      def getStart(s):#Zwraca id pola startu
            return s.__start
      
class PoolGUI(Listener):
      #Klasa, ktora umozliwia narysowanie pola
      __sl={30:"gray90",60:"gray60",90:"gray30",120:"#000000",2000:"red",4000:"#ffffff"}
      def __init__(s,C,pool,X=50,Y=50,a=20):
            #Dane:
            Listener.__init__(s)
            s.__C=C
            s.__pool=pool
            s.__X,s.__Y=X,Y
            s.__a=a
            #Definicje:
            s.__draw()
            s.listen2(pool)
      def __draw(s):#Rysuje pole
            i,j=s.__pool.getXY()
            s.__tag=s.__C.create_rectangle((i-0.5)*s.__a,(j-0.5)*s.__a,(i+0.5)*s.__a,(j+0.5)*s.__a,tag="board")
            s.__C.move(s.__tag,s.__X+s.__a*0.5,s.__Y+s.__a*0.5)
            s.__update()
      def __update(s):#Odswieza wyswietlanie punktu
            s.__updateWeight()
      def __updateWeight(s):#Odswieza wage pola
            w=s.__pool.getWeight()
            s.__C.itemconfig(s.__tag,fill=s.__sl[w])
      def receiveSignal(s,sender):#Odbiera sygnaly
            senderN=sender.getName()
            if senderN=="Pool":
                  s.__update()
class BoardGUI(Listener):
      #Klasa, ktor umozliwia narysowanie planszy
      def __init__(s,C,board,a):
            #Dane:
            Listener.__init__(s)
            s.__C=C
            s.__a=a
            s.__board=board
            #Definicje:
            s.__draw()
            s.listen2(board)
      def __draw(s):#Rysuje pola
            m,n=s.__board.getMN()
            for i in range(m):
                  for j in range(n):
                        pool=s.__board.getPoolWithXY(i,j)
                        PoolGUI(s.__C,pool,a=s.__a)
      def getC(s):#Zwraca id Canvasu
            return s.__C
      def getA(s):#Zwraca rozmiar pola
            return s.__a
class Player(Sender):
      #Klasa, ktora tworzy obiekt gracza
      def __init__(s,pool,color):
            #Dane:
            Sender.__init__(s)
            s.__previousWeight=None
            s.__pool=pool
            s.__color=color
      def setPool(s,pool):#Ustawia pole
            #musi zapamietac wage
            if s.__previousWeight==None:
                  pass
            else:
                  s.__pool.setWeight(s.__previousWeight)
            s.__pool=pool
            s.__previousWeight=pool.getWeight()
            s.__pool.setWeight(4000)
            
            s.sendSignal()
      def getPool(s):#Zwraca id pola na ktorym sie znajduje
            return s.__pool
      def getColor(s):#Zwraca kolor wypelnienia
            return s.__color
class Meta(Sender):
      #Klasa, ktora tworzy obiekt mety
      def __init__(s,pool):
            #Dane:
            Sender.__init__(s)
            s.__pool=pool
      def setPool(s,pool):#Ustawia pole
            s.__pool=pool
            s.sendSignal()
      def getPool(s):#Zwraca id pola na ktorym sie snajduje
            return s.__pool
class PlayerGUI(Listener):
      #Klasa, ktora umozlwia narysowanie gracza
      def __init__(s,C,player,r=10,color="gold",a=20):
            #Dane:
            Listener.__init__(s)
            s.__C=C
            s.__a=a
            s.__player=player
            s.__r=r
            #Definicje:
            s.__draw()
            s.listen2(player)
      def __draw(s):#Rysuje gracza
            x,y=s.__player.getPool().getXY()
            s.__tag=s.__C.create_oval((x+1)*s.__a-s.__r+4,(y+1)*s.__a-s.__r+4,(x+1)*s.__a+s.__r-4,(y+1)*s.__a+s.__r-4,fill=s.__player.getColor(),outline="brown")
            s.__C.move(s.__tag,50-s.__a*0.5,50-s.__a*0.5)
      def __update(s):#Odswieza rysunek gracza
            x,y=s.__player.getPool().getXY()
            s.__C.coords(s.__tag,(x+1)*s.__a-s.__r+4,(y+1)*s.__a-s.__r+4,(x+1)*s.__a+s.__r-4,(y+1)*s.__a+s.__r-4)
            s.__C.itemconfig(s.__tag,fill=s.__player.getColor())
            s.__C.move(s.__tag,50-s.__a*0.5,50-s.__a*0.5)
      def receiveSignal(s,sender):#Odbiera sygnaly
            senderN=sender.getName()
            if senderN=="Player":
                  s.__update()
class MetaGUI(Listener):
      #Klasa, ktora umozliwia narysowanie mety
      def __init__(s,C,meta,r=10,a=20):
            #Dane:
            Listener.__init__(s)
            s.__C=C
            s.__r=r
            s.__a=a
            s.__meta=meta
            #Definicje:
            s.__draw()
            s.listen2(meta)
      def __draw(s):#Rysuje mete
            x,y=s.__meta.getPool().getXY()
            s.__tag=s.__C.create_oval((x+1)*s.__a-s.__r+4,(y+1)*s.__a-s.__r+4,(x+1)*s.__a+s.__r-4,(y+1)*s.__a+s.__r-4,fill="",outline="brown",width=3)
            s.__C.move(s.__tag,50-s.__a*0.5,50-s.__a*0.5)
      def __update(s):#Odswieza rysunek mety
            x,y=s.__meta.getPool().getXY()
            s.__C.coords(s.__tag,(x+1)*s.__a-s.__r+4,(y+1)*s.__a-s.__r+4,(x+1)*s.__a+s.__r-4,(y+1)*s.__a+s.__r-4)
            s.__C.move(s.__tag,50-s.__a*0.5,50-s.__a*0.5)
      def receiveSignal(s,sender):#Odbiera sygnaly
            senderN=sender.getName()
            if senderN=="Meta":
                  s.__update()
class WayGUI:
      #Klasa, ktora umozliwia narysowanie drogi
      def __init__(s,C,pools):
            #Dane:
            s.__C=C
            s.__pools=pools
            #Definicje:
            s.__draw()
      def __getCoords(s):#Zwraca wspolrzedne sciezki
            coords=[]
            for i in s.__pools:
                  x,y=i.getXY()
                  coords.extend([x*20,y*20])
            return coords
      def __draw(s):#Rysuje sciezke
            if len(s.__pools)==0:
                  s.__tag=s.__C.create_line(0,0,0,0,arrow="last",width=2,fill="brown",dash=(5,10))
            else:
                  s.__tag=s.__C.create_line(*s.__getCoords(),arrow="last",width=2,fill="brown",dash=(5,10))
            s.__C.move(s.__tag,50,50)
            s.__C.lift(s.__tag)
      def __update(s):#Odswieza rysunek sciezki
            s.__C.coords(s.__tag,*s.__getCoords())
            s.__C.move(s.__tag,50+10,50+10)
            s.__C.lift(s.__tag)
      def setPools(s,pools):#Ustawia punkty
            s.__pools=pools
            s.__update()
        
from Tkinter import Canvas
class Desk:
      #Klasa, ktora rysuje Desk
      def __init__(s,master):
            #Dane:
            s.__master=master
            #Definicje:
            s.__draw()
      def __draw(s):#Rysuje Canvas
            s.__C=Canvas(s.__master,highlightthickness=0)
            s.__C.pack(side="top",expand=1,fill="both")
      def getC(s):#Zwraca id Canvasu
            return s.__C
from Tkinter import Tk
class Window:
      #Klasa, ktora rysuje okno
      def __init__(s,title,w,h,x,y):
            #Dane:
            s.__title=title
            s.__w,s.__h=w,h
            s.__x,s.__y=x,y
            #Definicje:
            s.__draw()
      def __draw(s):#Rysuje okno
            s.__master=Tk()
            s.__master.title(s.__title)
            s.__master.geometry("%sx%s+%s+%s"%(s.__w,s.__h,s.__x,s.__y))
      def getTitle(s):#Zwraca tytul
            return s.__title
      def setTitle(s,title):#Ustawia tytul
            s.__title=title
            s.__master.title(title)
      def loop(s):#Zapetla wyswietlanie okna
            s.__master.mainloop()
      def getMaster(s):#Zwraca id okna
            return s.__master
class CurrentWeight(Listener):
      #Kontrolka, ktora wyswietla biezaca wage
      __sl={30:"gray90",60:"gray60",90:"gray30",120:"#000000",2000:"red",4000:"#ffffff"}
      def __init__(s,C,game):
            #Dane:
            Listener.__init__(s)
            s.__C=game.getC()
            s.__game=game
            #Definicje:
            s.__draw()
            s.listen2(game)
      def __draw(s):#Rysuje pole
            s.__tag=s.__C.create_oval(0,0,50,50,fill="gray90")
      def __update(s):#Odswieza kontrolke
            s.__C.itemconfig(s.__tag,fill=s.__sl[s.__game.getCurrentWeight()])
      def receiveSignal(s,sender):#Odbiera sygnaly
            if sender.getName()=="Game":
                  s.__update()
                  
from random import choice
class Game(Sender):
      def __init__(s,C,m=20,n=20,xM=1,yM=1):
            #Dane:
            Sender.__init__(s)
            s.__currentWeight=30
            s.__board=Board(m,n)
            s.__C=C
            s.__wayG=WayGUI(C,[])
            boardG=BoardGUI(s.__C,s.__board,20)
            s.__putPlayer(0,0,"orange")
            s.__putAgent(0,3,"violet")
            s.__putMeta(xM,yM)
            #Definicje:
            s.__bind()
      def __putPlayer(s,x,y,color):#Ustawia gracza
            s.__player=Player(s.__board.getPoolWithXY(x,y),color)
            PlayerGUI(s.__C,s.__player)
      def __putAgent(s,x,y,color):#Ustawia gracza
            s.__agent=Player(s.__board.getPoolWithXY(x,y),color)
            PlayerGUI(s.__C,s.__agent)
      def __putMeta(s,x,y):#Ustawia mete
            s.__meta=Meta(s.__board.getPoolWithXY(x,y))
            MetaGUI(s.__C,s.__meta)
      def __animateMotion(s):#Animuje przejscie gracza
            pools=s.__board.shortestPath(s.__player.getPool(),s.__meta.getPool())
            agentGoal=choice(s.__board.getPools())
            pools2=s.__board.shortestPath(s.__agent.getPool(),agentGoal)
            po=[pools[0]]
            
            n=len(pools[1:])
            m=len(pools2[1:])
            i=0
            j=0
            while pools[-1]!=s.__player.getPool():
            #for i in range(max([n+1,m+1])):#pools[1:]:
                  if i<=n:
                        if j<=m:
                              if pools[i]!=pools2[j]:
                                    s.__player.setPool(pools[i])
                                    po.append(pools[i])
                                    if len(po)>=2:
                                          s.__wayG.setPools(po)
                                    else:
                                          pass
                              else:
                                    pools=s.__board.shortestPath(pools[i-1],s.__meta.getPool())
                                    i=0
                        else:
                              s.__player.setPool(pools[i])
                              po.append(pools[i])
                              if len(po)>=2:
                                    s.__wayG.setPools(po)
                              else:
                                    pass
                  else:
                        pass
                  
                  if j<=m:
                        if i<=n:
                              if pools[i]!=pools2[j]:
                                    s.__agent.setPool(pools2[i])
                              else:
                                    print "Agent gottcha!"
                                    pools2=s.__board.shortestPath(pools2[j-1],agentGoal)
                                    j=0
                  else:
                        pass
                  s.__C.after(200)
                  s.__C.update()
                  i+=1
                  j+=1
            s.__wayG.setPools(pools)
            
      def getC(s):#Zwraca id Canvasu
            return s.__C
      def getCurrentWeight(s):#Zwraca biezaca wage
            return s.__currentWeight
      def setCurrentWeight(s,weight):#Ustawia bezaca wage
            s.__currentWeight=weight
            s.sendSignal()
      def __setMeta(s,event):#Ustawia mete na planszy
            s.__meta.setPool(s.__board.getPoolWithXY((event.x-50)/20,(event.y-50)/20))
            s.__animateMotion()
      def __setPoolWeight(s,event):#Ustawia wage pola
            X,Y=(event.x-50)/20,(event.y-50)/20
            pool=s.__board.getPoolWithXY(X,Y)
            pool.setWeight(s.__currentWeight)
      def __bind(s):#Tworzy bindowanie
            s.__C.focus_set()
            s.__C.bind("<KeyRelease-1>",lambda e:s.setCurrentWeight(30))
            s.__C.bind("<KeyRelease-2>",lambda e:s.setCurrentWeight(60))
            s.__C.bind("<KeyRelease-3>",lambda e:s.setCurrentWeight(90))
            s.__C.bind("<KeyRelease-4>",lambda e:s.setCurrentWeight(120))
            s.__C.bind("<KeyRelease-4>",lambda e:s.setCurrentWeight(2000))
            s.__C.tag_bind("board","<2>",s.__setMeta)
            s.__C.tag_bind("board","<1>",s.__setPoolWeight)
class Main:
      #Glowna klasa
      def __init__(s):
            #Dane:
            win=Window("Way",600,600,0,0)
            desk=Desk(win.getMaster())
            C=desk.getC()
            game=Game(C,m=20,n=20)
            CurrentWeight(C,game)
            #Definicje:
            win.loop()
            
Main()