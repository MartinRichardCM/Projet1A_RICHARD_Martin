from PIL import Image as img
import numpy as np
import cmath
from matplotlib.pyplot import imread
import matplotlib.pyplot as plt
from scipy import fftpack as fft






## Définition des grandeurs mises en jeu & des images

# ATTENTION : IMAGES EN PNG UNIQUEMENT, ON POURRAIT FAIRE UNE RENORMALISATION POUR LES JPG POUR QUE CA MARCHE


im1 = imread('/Users/richardmartin/Documents/la Joconde.png')
im2 = imread('/Users/richardmartin/Documents/Huygens.png')
im3 = imread('/Users/richardmartin/Documents/fourier.png')
im4 = imread('/Users/richardmartin/Documents/Tesla.png')

# Attention à ce que les tailles d'images ne soient pas trop différentes, même si un des programmes redimensionne.

im = [im1,im2,im3,im4]
n = 4                     # Le nombre d'images
m = 800                    # Nombre de barreau de la grille

x = 222                   # Position en x du décalage du trou par rapport au centre
y = 274                 # Position en y du décalage du trou par rapport au centre
r = 100                  # Rayon du trou



## Partie I : Programmes


def maximum(L):
    #Retourne le maximum de la liste L.

    a = 0
    for k in range (len(L)):
        if L[k] > a:
            a = L[k]
    return(a)


def minimum(L):
    # Retourne le minimum de la liste L.

    a = 0
    for k in range(len(L)):
        if L[k] < a:
            a = L[k]
    return(a)


def liste_ligne(M):
    #Retourne la liste des longueurs de lignes de M.

    L = []
    for k in range (len(M)):
        L.append(len(M[k]))
    return(L)


def liste_colonne(M):
    #Retourne la liste des longueurs de colonnes de M.

    L = []
    for k in range (len(M)):
        L.append(len(M[k][0]))
    return(L)


def taille(M):
    # Retourne le maximum des maximum de longueur de colonnes et de lignes de M.

    c = maximum(liste_ligne(M))
    d = maximum(liste_colonne(M))
    return(np.max([c,d]))


def tableau_blanc(a,b):
    # Renvoie une image blanche de la taille des longueur et largeur d'une image d'entrée.

    N = np.zeros((a,b))
    for i in range (a):
        for j in range (b):
            N[i][j] = 255

    return(N)


def meme_taille(M):
    # Permet de redimensionner 2 images différentes à la même taille.

    a=taille(M)
    N=[]

    for k in range(len(M)):

        if len(M[k])<a and len(M[k][0])<a:

            b=a-len(M[k])
            c=a-len(M[k][0])

            if c%2==0 and b%2==0:

                d=b//2
                e=c//2
                Q=np.ones((len(M[k]),e))
                R=np.concatenate((M[k],Q),axis=1)
                S=np.concatenate((Q,R),axis=1)
                L=np.ones((d,len(S[0])))
                T=np.concatenate((S,L))
                N.append(np.concatenate((L,T)))

            elif b%2==0 and c%2!=0:

                d=b//2
                e=c//2
                Q=np.ones((len(M[k]),e))
                R=np.ones((len(M[k]),e+1))
                S=np.concatenate((M[k],Q),axis=1)
                T=np.concatenate((R,S),axis=1)
                L=np.ones((d,len(T[0])))
                U=np.concatenate((T,L))
                N.append(np.concatenate((L,U)))

            elif b%2!=0 and c%2==0:

                d=b//2
                e=c//2
                R=np.ones((len(M[k]),e))
                S=np.concatenate((M[k],R),axis=1)
                T=np.concatenate((R,S),axis=1)
                L=np.ones((d,len(T[0])))
                Q=np.ones((d+1,len(T[0])))
                U=np.concatenate((T,L))
                N.append(np.concatenate((Q,U)))

            elif b%2!=0 and c%2!=0:

                d=b//2
                e=c//2
                R=np.ones((len(M[k]),e))
                S=np.ones((len(M[k]),e+1))
                T=np.concatenate((M[k],R),axis=1)
                U=np.concatenate((S,T),axis=1)
                L=np.ones((d,len(U[0])))
                Q=np.ones((d+1,len(U[0])))
                V=np.concatenate((U,L))
                N.append(np.concatenate((Q,V)))

        elif len(M[k])<a:

            b=a-len(M[k])

            if b%2==0:

                c=b//2
                L=np.ones((c,len(M[k][0])))
                Q=np.concatenate((M[k],L))
                N.append(np.concatenate((L,Q)))

            else:

                c=b//2
                L=np.ones((c,len(M[k][0])))
                Q=np.ones((c+1,len(M[k][0])))
                R=np.concatenate((M[k],L))
                N.append(np.concatenate((R,Q)))

        elif len(M[k][0])<a:

            b=a-len(M[k][0])

            if b%2==0:

                c=b//2
                L=np.ones((len(M[k]),c))
                Q=np.concatenate((M[k],L),axis=1)
                N.append(np.concatenate((L,Q),axis=1))

            else:

                c=b//2
                L=np.ones((len(M[k]),c))
                Q=np.ones((len(M[k]),c+1))
                R=np.concatenate((M[k],L),axis=1)
                N.append(np.concatenate((Q,R),axis=1))

        else:

            N.append(M[k])

    return(N)



def TF(M):
    # Calcule la FFT d'une image.

    im1 = np.fft.fft2(M)
    im1 = np.fft.fftshift(im1)  #Décale les basses fréquences au centre
    return(im1)


def TFinverse(M):
    # Calcule la FFT^(-1) d'une image.

    im2 = np.fft.ifft2(M)
    return(im2)


def direction(M,theta):
    # Fait une rotation de l'image M de theta.

    A = img.fromarray(M)
    B = A.rotate(theta)
    return(np.array(B))


def directionbis(M,theta):
    A = nuance_de_gris(M)
    B = img.fromarray(A)
    C=B.rotate(theta)
    return (np.array(C))


def correction(M):
    # Différencie les noirs de l' intrisèque et des bords ajoutés.

    (a,b) = (len(M),len(M[0]))
    N = np.zeros((a,b))

    for i in range (a):
        for j in range (b):
            if M[i][j] == 0:
                N[i][j] = 0.1
            else:
                N[i][j] = M[i][j]
    return(N)


def invertion(M):
    # Renvoie l' M en négatif.

    (a,b) = (len(M),len(M[0]))
    N = np.zeros((a,b))

    for i in range(a):
        for j in range(b):
            N[i][j] = 1-M[i][j]
    return(N)


def anti_correction(M):
    # Inverse de correction.

    (a,b) = (len(M),len(M[0]))
    N = np.zeros((a,b))

    for i in range(a):
        for j in range(b):
            if M[i][j] == 0.1:
                N[i][j] = 0
            else:
                N[i][j] = M[i][j]
    return(N)


def anti_bord(M):
    # Ajoute des bords blancs à la place des bords noirs.

    N = np.zeros((len(M),len(M[0])))
    for i in range (len(M)):
        for j in range (len(M[0])):
            if M[i][j] == 0:
                N[i][j] = 1
            else:
               N[i][j] = M[i][j]
    return(N)


def image_rotation(M,p):
    # Organise la rotation des images en fonction du nombre de celles-ci.

    theta = (190/n)*(p)
    return(direction(M,theta))


def image_rotationbis(M,p):
    # Organise la rotation des images en fonction du nombre de celles-ci.

    theta = (190/n)*(p)
    return(directionbis(M,(-theta)))


def nuance_de_gris(M):
    #fonctionne
    dim = np.shape(M)

    if len(dim) == 2:
        return(M)
    else :
        tab = 0.299 * M[:,:,0] + 0.587 * M[:,:,1] + 0.114 * M[:,:,2]
    return(tab)


def gris(M):
    # Renvoie une liste d'images par la même liste d'images en nuances de gris.

    a = len(M)
    N = []

    for k in range (a):
        N.append(noir_et_blanc(M[k]))
    return(N)


def partie_entiere(a):
    #Renvoie l'entier le plus proche de a.

    b = a%1
    if b > 0.5:
        a = int(a)+1
    else:
        a = a
    return(a)


def format(M):
    # Renvoie un binaire correspondant.

    for i in range (len(M)):
        for j in range (len(M[0])):
            if M[i][j] > 2:
                return(1)
    return(0)


def to_png(M):
    #Renormalise pour des images passant de jpeg à png.

    if format(M) == 1:
        (a,b) = (len(M),len(M[0]))
        N = np.zeros((a,b))

        for i in range (a):
            for j in range (b):
                N[i][j] = (M[i][j])/255
        return(N)
    return(M)


def noir_et_blanc(M):
    # Renvoie l'image en noir et blanc d'une image en nuances de gris.

    P = np.ones((len(M),len(M[0])))
    N = nuance_de_gris(M)

    for i in range (len(M)):
        for j in range (len(M[0])):
            a = N[i][j]
            if a < 0.65:
                P[i][j] = 0
    return(P)


def niveau_noir(M,p):

    N = np.zeros((len(M),len(M[0])))
    for i in range (len(M)):
        for j in range (len(M[0])):

            #if M[i][j]!= 1:
            N[i][j] = (N[i][j])/p
    return(M)


def sommation_finale(W,n):
    #ici, W est la liste d'images en noir et blanc et n=len(W), le nombre d'images.

    N = niveau_noir(W[0],n)

    for k in range (1,n):
        N = N+niveau_noir(W[k],n)
    return(N)


def recopiage(M):
    # Recopie M

    N = []
    for k in range (len(M)):
        N.append(M[k][:])
    return(N)


def images_transformees(W,m,n):
    # W est ici une liste d'images DE MËME FORMAT et la fonction renvoie la liste
    # d'images qu'il ne reste plus qu'à sommer.

    N = []
    A = grille_fin (len(W[0]),m)
    c = 0

    for k in range (n):
        M = recopiage(N)
        B = A*W[k]
        C = correction(B)
        D = image_rotation (C,k)
        E = anti_bord(D)
        F = anti_correction(E)
        G = invertion(F)
        N.append(G)
        H = im_fft(G)
        I = np.hstack((G,H))
        c = c+1
    return(N)


def spectre(M):
    # Calcule le spectre d'une image (pour la FFT).

    # for i in range(len(M)):
    #     for j in range(len(M[0])):
    #         if M[i][j] < 10**(-10):
    #             M[i][j] = 1*10**(-6)

    Spectre = 20*np.log(np.abs(M))
    return(Spectre)


def im_fft_plot(im):
    # Calcule le spectre de la FFT d'une image.

    im1 = np.fft.fft2(nuance_de_gris(im))
    im1 = np.fft.fftshift(im1)

    Spectre = 20*np.log(np.abs(im1))
    return(Spectre)


def im_fft(im):
    # Calcule la FFT d'une image.

    im1 = np.fft.fft2(nuance_de_gris(im))
    im1 = np.fft.fftshift(im1)              # Amène les basses fréquences au centre

    return(im1)


def fft_im(im):
    # Calcule la FFT^(-1) d'une image.

    im2 = np.fft.ifftshift(nuance_de_gris(im))
    im2 = np.abs(np.fft.ifft2(im))

    return(im2)


def grille(a,m):
    # Réalise la grille en fonction de m le nombre de barreaux.

    N = [0]*(a)
    b = partie_entiere(a/m)

    for j in range (m):
        if j%2 == 0 and b+j*b < a:
            for k in range (int(b)):
                c = int(j*b+k)
                N[c] = 1
    return(N)


def grille_fin (a,m):
    # M est ici une ligne (cf la fonction grille).
    # N est la liste d'image redimentionnée (homogène au niveau des dimentions).

    M = grille(a,m)
    P = np.zeros((a,a))

    for i in range (a):
        for j in range (a):
            P[i][j] = M[j]
    return(P)


def Masque_cercle_n(M,x,y,r):
    # Renvoie l'image d'un trou de rayon r déplacé par rapport au centre de x et y.

    (u,v) = (len(M),len(M[0]))
    masque = np.zeros((u,v))

    for i in range(-r, r+1):
        for j in range(-r, r+1):
            if i**2 + j**2 <= r**2 :
                masque[u//2+x+i,v//2+y+j] = 1

    return(masque)


def filtrage(M,x,y,r):
    # Réalise le filtrage de la FFT dans le plan de Fourier par le trou.

    (u,v) = (len(M),len(M[0]))
    N = Masque_cercle_n(M,x,y,r)

    for i in range(u):
        for j in range(v):
            if N[i][j] != 1:
                M[i][j] = 0
    return(M)



## Partie II : Calculs sur les images & Plot

imbis=[image_rotationbis(im1,0),image_rotationbis(im2,1),image_rotationbis(im3,2),image_rotationbis(im4,3)]
G = gris(imbis)
H = meme_taille(G)
I = images_transformees(H,m,n)
J = sommation_finale(I,n)
K = invertion(J)

A = filtrage(im_fft(K),x,y,r)
B = fft_im(A)


max = maximum(K[0])
for j in range(len(K)):

    max2 = maximum(K[j])
    if max2 > max:
        max = max2


H = np.hstack((np.uint8(255/max*K),im_fft_plot(K),spectre(A),spectre(B)))

dim = np.shape(H)

# pyplot.text(dim[0]//2, dim[0] + 700, 'Images superposées en négatif', horizontalalignment = 'center', fontsize = 10, style ='italic', family = 'serif')
# pyplot.text((3/2) * dim[0], dim[0] + 700, ' images superposées', horizontalalignment = 'center', fontsize = 10, style ='italic', family = 'serif')
# pyplot.text((5/2) * dim[0], dim[0] + 700, 'Filtrage de la TF', horizontalalignment = 'center', fontsize = 10, style ='italic', family = 'serif')
# pyplot.text((7/2) * dim[0], dim[0] + 700, 'Photo sur écran', horizontalalignment = 'center', fontsize = 10, style ='italic', family = 'serif')


plt.axis('off')
plt.imshow(K,cmap='gray')
plt.show()

plt.imshow(H,cmap='gray')
plt.show()

plt.imshow(Masque_cercle_n(K,x,y,r),cmap='gray')
plt.show()

################################################################################
#Sinbad the sailor, Schtroumpf farceur
################################################################################