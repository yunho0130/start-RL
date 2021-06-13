def reward_function(params):
    
    # 딥레이서 관련 파라미터 읽어오기
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    
    # 중앙선과의 거리에 따라 마커 3개를 설정
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width
    
    # 차량이 중앙선에 가까우면 보상을 크게, 멀면 보상을 작게
    if distance_from_center <= marker_1:
        reward = 1.0
    elif distance_from_center <= marker_2:
        reward = 0.5
    elif distance_from_center <= marker_3:
        reward = 0.1
    else:
        reward = 1e-3  # 오프 트랙 혹은 충돌
    
    return float(reward)