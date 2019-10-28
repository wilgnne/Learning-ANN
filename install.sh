echo "Install dependencies"
sudo pip3.7 install numpy || sudo pip3 install numpy

echo "Install Neural Network - Wilgnne K."

path="$(python3.7 -m site --user-site)"

sudo rm -r $path/NeuralNetwork;

sudo git clone https://github.com/Wilgnne/Learning-ANN.git $path/NeuralNetwork