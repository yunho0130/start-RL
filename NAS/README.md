## NAS 디렉토리 구성
NAS 디렉토리는 Do It! RL 도서의 NAS의 실습에 필요한 파일들이 저장되어 있습니다. 파일의 구성은 아래와 같습니다.
|파일이름|설명|
|--|--|
|datasets.py|CIFAR-10 데이터를 다운로드 하고 학습에 필요한 형태로 변환|
|macro.py|매이크로 탐색 공간을 활용한 ENAS 학습|
|micro.py|마이크로 탐색 공간을 활용한 ENAS 학습|
|ops.py|탐색 공간에서 선택할 수 있는 합성곱 연산자 정의|
|retrain.py|학습된 신경망을 가지고 모델을 학습|
|search.py|ENAS 학습을 위한 코드|
|utils.py|학습에 필요한 각종 기능들|

## NNI ENAS 실습 실행 과정
NNI ENAS 실습을 위해서 아래와 같은 환경을 구성합니다.

 - Anaconda를 활용한 가상환경 구성
 - 텐서플로우 GPU 2.1 설치
 - 파이토치 1.4 및 토치비젼 0.5 설치
 - NNI v1.7 설치하기 및 NNI 소스코드 Git Clone
 - NNI ENAS 실행하기

#### Anaconda를 활용한 가상환경 구성
먼저, Anaconda에 NNI ENAS 실습을 위한 환경을 구성합니다. Python 3.7로 환경을 구성하도록 하겠습니다.
```
conda create -n nni_final pip python=3.7
```
가상 환경을 활성화 한 후에 텐서플로우 GPU 2.1을 설치 합니다.
```
conda activate nni_final
```
### 텐서플로우 GPU 2.1 설치
pip로 텐서플로우를 설치 합니다.
```
pip install --ignore-installed --upgrade https://storage.googleapis.com/tensorflow/windows/gpu/tensorflow_gpu-2.1.0-cp37-cp37m-win_amd64.whl`
```
>  OS별 텐서플로우 GPU 버전 설치 패키지 설치하기
> - Windows: https://storage.googleapis.com/tensorflow/windows/gpu/tensorflow_gpu-2.1.0-cp37-cp37m-win_amd64.whl
> - Linux: https://storage.googleapis.com/tensorflow/linux/gpu/tensorflow_gpu-2.1.0-cp37-cp37m-manylinux2010_x86_64.whl
> - macOS: https://storage.googleapis.com/tensorflow/mac/cpu/tensorflow-2.1.0-cp37-cp37m-macosx_10_9_x86_64.whl (CPU만 지원)

정상적으로 설치가 되었는지 파이썬 명령어로 확인할 수 있습니다.
 ```
 python -c "import tensorflow as tf;print(tf.reduce_sum(tf.random.normal([1000, 1000])))"
 ```

###  파이토치 1.4 및 토치비젼 0.5 설치
파이토치는 파이토치 홈페이지(https://pytorch.org/)에서 원하는 환경에 맞는 설치 명령어를 생성해서 사용할 수 있습니다. 
```
pip install torch===1.4.0 torchvision===0.5.0 -f https://download.pytorch.org/whl/torch_stable.html
```
파이썬 인터렉티브 모드를 사용해서 정상 설치를 확인해 보겠습니다.
```
python
Python 3.7.7 (default, May  6 2020, 11:45:54) [MSC v.1916 64 bit (AMD64)] :: Anaconda, Inc. on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> import torch
>>> torch.cuda.get_device_name(0)
'GeForce GTX 1650'
>>> torch.cuda.is_available()
True
>>> print(torch.__version__)
1.4.0
>>> quit()
```
### NNI v1.7 설치하기 및 NNI 소스코드 Git Clone
NNI 역시 pip로 설치를 합니다. NNI를 실습할 수 있는 NNI 예제가 포함된 NNI 소스코드는 git clone으로 다운로드 받습니다.
```
pip install --upgrade nni==1.7
git clone -b v1.7 https://github.com/microsoft/nni.git
```
NNI가 정상적으로 설치가 되었는지 예제를 통해서 확인해 보겠습니다.
```
nnictl create --config nni/examples/trials/mnist-tfv2/config_windows.yml
```
> Mac OS, Linux 실행
>  - nnictl create --config nni/examples/trials/mnist-tfv2/config.yml

NNI 실행을 확인하였다면 NNI 실행을 중지 해 줍니다.
```
nnictl stop
```
#### NNI ENAS 실행하기
NNI에 포함된 ENAS를 실행해 보겠습니다. 2개의 탐색 공간에 대해서 학습을 진행해 보도록 하겠습니다.
- 매크로 탐색 공간을 활용한 ENAS
- 마이크로 탐색 공간을 활용한 ENAS

##### 매크로 탐색 공간을 활용한 ENAS 실행
```
cd nni/examples/nas/enas
python search.py --search-for macro
```

빠른 결과 확인을 위해서 학습 에폭을 줄여 봅시다. **--epochs** 옵션을 사용합니다.
```
python search.py --search-for macro --epochs 2
```
##### 마이크로 탐색 공간을 활용한 ENAS 실행
매크로 탐색 공간과 동일한 실행 파일을 사용하며 **--search-for** 옵션의 값을 **micro**로 변경합니다.
```
python search.py --search-for micro
```

빠른 결과 확인을 위해서 학습 에폭을 줄여 봅시다. **--epochs** 옵션을 사용합니다.
```
python search.py --search-for micro --epochs 2
```
#### ENAS에서 생성된 신경망 구조를 활용한 재학습
ENAS로 만들어진 신경망 구조를 사용하여 모델을 생성할 수 있습니다.  이 Git Repo의 파일을 사용하여 ENAS 학습과 재학습을 진행하시면 됩니다.
```
python search.py --search-for micro
python retrain.py --search-for micro
```
