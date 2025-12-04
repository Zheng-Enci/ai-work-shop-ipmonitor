<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IP出现次数统计</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: "Microsoft YaHei", Arial, sans-serif;
        }
        body {
            background-color: #f8f9fa;
            padding: 20px;
        }
        .header-container {
            position: relative;
            margin-bottom: 30px;
        }
        .scan-stats {
            color: #666;
            font-size: 16px;
            font-weight: 600;
            position: absolute;
            top: 0;
            left: 0;
        }
        h1 {
            text-align: center;
            color: #333;
            margin: 0;
            padding: 10px 0;
        }
        .ip-table {
            width: 90%;
            margin: 0 auto;
            border-collapse: collapse;
            background-color: #fff;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .ip-table td {
            width: 10%;
            height: 60px;
            text-align: center;
            border: 1px solid #ddd;
            padding: 5px;
            font-size: 14px;
            position: relative;
        }
        .ip-table .ip-number {
            font-weight: bold;
            margin-bottom: 5px;
            display: block;
        }
        .ip-table .count-number {
            font-size: 16px;
            font-weight: 600;
        }
        /* 0次：白色背景 */
        .count-zero {
            background-color: #ffffff !important;
        }
        .count-zero .ip-number,
        .count-zero .count-number {
            color: #718096 !important;
        }
        /* 非坊内IP：斜纹背景 */
        .non-fang { 
            background: repeating-linear-gradient(
                45deg,
                #f5f5f5,
                #f5f5f5 8px,
                #e8e8e8 8px,
                #e8e8e8 16px
            ) !important;
            border: 2px dashed #cccccc !important;
            opacity: 0.7;
        }
        .non-fang .ip-number {
            color: #999999 !important;
            font-weight: normal;
        }
        .legend {
            width: 90%;
            margin: 20px auto 0;
            display: flex;
            justify-content: center;
            gap: 20px;
            flex-wrap: wrap;
            background-color: #fff;
            padding: 10px;
            border-radius: 4px;
            box-shadow: 0 1px 5px rgba(0,0,0,0.1);
        }
        .legend-item {
            display: flex;
            align-items: center;
            gap: 5px;
            font-size: 13px;
        }
        .legend-color {
            width: 20px;
            height: 20px;
            border-radius: 2px;
        }
        .legend-color.non-fang {
            background: repeating-linear-gradient(
                45deg,
                #f5f5f5,
                #f5f5f5 4px,
                #e8e8e8 4px,
                #e8e8e8 8px
            );
            border: 2px dashed #cccccc;
        }
        /* 颜色筛选横条样式 */
        .color-filter-container {
            width: 90%;
            margin: 20px auto;
            background-color: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .color-filter-title {
            text-align: center;
            color: #333;
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 15px;
        }
        .color-filter-bar {
            display: flex;
            width: 100%;
            gap: 2px;
            margin-bottom: 10px;
        }
        .color-block-wrapper {
            flex: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .color-block {
            width: 100%;
            height: 40px;
            transition: all 0.2s ease;
            border-radius: 4px;
            position: relative;
            cursor: pointer;
            box-shadow: 0 1px 3px rgba(0,0,0,0.2);
        }
        .color-block:hover {
            transform: scaleY(1.1);
            z-index: 1;
            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        }
        .color-block.selected {
            border: 3px solid #1890ff;
            box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.3), 0 2px 8px rgba(0,0,0,0.3);
            z-index: 2;
        }
        .color-block-label {
            margin-top: 5px;
            font-size: 11px;
            color: #666;
            text-align: center;
            white-space: nowrap;
            font-weight: 500;
        }
        @media (max-width: 768px) {
            .color-block-label {
                font-size: 9px;
            }
        }
        .color-filter-controls {
            display: flex;
            justify-content: center;
            gap: 10px;
            margin-top: 15px;
        }
        .filter-btn {
            padding: 8px 20px;
            background-color: #1890ff;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            transition: background-color 0.2s ease;
        }
        .filter-btn:hover {
            background-color: #40a9ff;
        }
        .filter-btn:active {
            background-color: #096dd9;
        }
        /* 筛选状态下的IP单元格样式 */
        .ip-table td.filtered-out {
            opacity: 0.25;
            filter: grayscale(50%);
            transition: opacity 0.3s ease, filter 0.3s ease;
        }
        .ip-table td.filtered-in {
            opacity: 1;
            filter: brightness(1.1);
            transition: opacity 0.3s ease, filter 0.3s ease;
        }
    </style>
</head>
<body>
    <div class="header-container">
        <div class="scan-stats">最近7天扫描次数：{{ recent_7d_scans }}</div>
        <h1>IP出现次数统计</h1>
    </div>

    <table class="ip-table">
        {% set max_count = 0 %}
        {% for ip_str, count in ip_counter.items() %}
            {% if count > max_count %}
                {% set max_count = count %}
            {% endif %}
        {% endfor %}
        {% for row in range(10) %}
        <tr>
            {% for col in range(10) %}
                {% set current_ip = 151 + row*10 + col %}
                {% set current_ip_str = "10.0.48." + current_ip|string %}
                {% set current_count = ip_counter.get(current_ip_str, 0) %}
                
                {% if current_ip not in fang_ips %}
                    {# 非坊内IP #}
                    <td class="non-fang">
                        <span class="ip-number">{{ current_ip }}</span>
                    </td>
                {% elif current_count == 0 %}
                    {# 0次：白色背景 #}
                    <td class="count-zero">
                        <div>
                            <span class="ip-number">{{ current_ip }}</span>
                            <span class="count-number">{{ current_count }}</span>
                        </div>
                    </td>
                {% else %}
                    {# 有次数：使用JavaScript动态计算颜色 #}
                    <td class="heatmap-cell" data-ip="{{ current_ip }}" data-count="{{ current_count }}">
                        <div>
                            <span class="ip-number">{{ current_ip }}</span>
                            <span class="count-number">{{ current_count }}</span>
                        </div>
                    </td>
                {% endif %}
            {% endfor %}
        </tr>
        {% endfor %}
    </table>

    <!-- 颜色筛选横条 -->
    <div class="color-filter-container" id="colorFilterContainer" style="display: none;">
        <div class="color-filter-title">点击颜色筛选IP范围</div>
        <div class="color-filter-bar" id="colorFilterBar"></div>
        <div class="color-filter-controls">
            <button class="filter-btn" id="resetFilterBtn">显示全部</button>
        </div>
    </div>

    <div class="legend">
        {% if max_count > 0 %}
        <div class="legend-item">
            <div class="legend-color" style="background: linear-gradient(to right, rgb(255,218,185), rgb(255,69,0));"></div>
            <span>1次-{{ max_count }}次（坊内，颜色越深次数越多）</span>
        </div>
        {% endif %}
    </div>
    
    <!-- 调试信息 -->
    <div style="margin-top: 20px; padding: 10px; background: #f0f0f0; text-align: center; font-size: 12px; color: #666;">
        最大次数: {{ max_count }} | 
        {% if max_count > 0 %}
            示例：1次=rgb(255,218,185), {{ max_count }}次=rgb(255,69,0) | 
            总IP数: {{ ip_counter|length }}
        {% else %}
            暂无数据
        {% endif %}
    </div>
</body>
<script>
    // 定义坊内IP列表（从服务器端渲染）
    const fangIps = {{ fang_ips|tojson }};
    
    // IP计数器数据（从服务器端渲染）
    const ipCounter = {{ ip_counter|tojson }};
    
    /**
     * 将当前值映射到0-255范围
     * @param {number} minValue - 最小值
     * @param {number} maxValue - 最大值
     * @param {number} currentValue - 当前值
     * @returns {number} 0-255之间的整数值
     */
    function mapTo255(minValue, maxValue, currentValue) {
        // 如果最大值和最小值相等，返回中间值
        if (maxValue === minValue) {
            return 128;
        }
        
        // 线性映射：将[currentValue]映射到[0, 255]
        // 公式：result = (currentValue - minValue) / (maxValue - minValue) * 255
        let mapped = ((currentValue - minValue) / (maxValue - minValue)) * 255;
        
        // 确保返回值在0-255范围内
        mapped = Math.max(0, Math.min(255, mapped));
        
        // 返回整数
        return Math.round(mapped);
    }
    
    // 全局变量：存储颜色范围数据
    let globalMinCount = 0;
    let globalMaxCount = 0;
    let colorBlockCount = 15; // 颜色块数量
    let selectedColorRange = null; // 当前选中的颜色范围
    
    /**
     * 计算颜色RGB值
     */
    function calculateColor(minCount, maxCount, count) {
        const lightOrange = { r: 255, g: 218, b: 185 };
        const darkOrange = { r: 255, g: 69, b: 0 };
        
        if (maxCount === minCount) {
            return lightOrange;
        }
        
        const intensity = mapTo255(minCount, maxCount, count);
        const r = Math.round(lightOrange.r - (intensity / 255) * (lightOrange.r - darkOrange.r));
        const g = Math.round(lightOrange.g - (intensity / 255) * (lightOrange.g - darkOrange.g));
        const b = Math.round(lightOrange.b - (intensity / 255) * (lightOrange.b - darkOrange.b));
        
        return { r, g, b };
    }
    
    /**
     * 应用热力图颜色到所有IP单元格
     */
    function applyHeatmapColors() {
        // 收集所有有次数的IP数据
        const counts = [];
        const heatmapCells = document.querySelectorAll('.heatmap-cell');
        
        heatmapCells.forEach(cell => {
            const count = parseInt(cell.getAttribute('data-count')) || 0;
            if (count > 0) {
                counts.push(count);
            }
        });
        
        if (counts.length === 0) {
            return; // 没有数据
        }
        
        // 找到最小值和最大值
        globalMinCount = Math.min(...counts);
        globalMaxCount = Math.max(...counts);
        
        // 定义颜色范围：从浅橙色(255,218,185)到深橙色/红色(255,69,0)
        const lightOrange = { r: 255, g: 218, b: 185 };  // 浅橙色 (PeachPuff)
        const darkOrange = { r: 255, g: 69, b: 0 };      // 深橙红色 (OrangeRed)
        
        // 为每个单元格计算和应用颜色
        heatmapCells.forEach(cell => {
            const count = parseInt(cell.getAttribute('data-count')) || 0;
            
            if (count === 0) {
                return; // 0次已经在模板中处理了
            }
            
            // 使用mapTo255计算颜色强度（次数越多，强度值越大，颜色越深）
            const intensity = mapTo255(globalMinCount, globalMaxCount, count);
            
            // 反向映射：intensity越大（次数越多），颜色越深
            const r = Math.round(lightOrange.r - (intensity / 255) * (lightOrange.r - darkOrange.r));
            const g = Math.round(lightOrange.g - (intensity / 255) * (lightOrange.g - darkOrange.g));
            const b = Math.round(lightOrange.b - (intensity / 255) * (lightOrange.b - darkOrange.b));
            
            // 设置背景颜色
            const bgColor = `rgb(${r}, ${g}, ${b})`;
            cell.style.backgroundColor = bgColor;
            
            // 计算亮度来决定文字颜色
            const brightness = r * 0.299 + g * 0.587 + b * 0.114;
            const textColor = brightness < 180 ? 'white' : '#333333';
            
            // 设置文字颜色
            const ipNumber = cell.querySelector('.ip-number');
            const countNumber = cell.querySelector('.count-number');
            if (ipNumber) ipNumber.style.color = textColor;
            if (countNumber) countNumber.style.color = textColor;
        });
        
        // 创建颜色横条
        createColorBar();
    }
    
    /**
     * 创建颜色筛选横条
     */
    function createColorBar() {
        if (globalMaxCount === 0) {
            return; // 没有数据，不显示颜色横条
        }
        
        const colorFilterBar = document.getElementById('colorFilterBar');
        const colorFilterContainer = document.getElementById('colorFilterContainer');
        
        // 清空现有颜色块
        colorFilterBar.innerHTML = '';
        
        // 显示颜色筛选容器
        colorFilterContainer.style.display = 'block';
        
        // 计算每个颜色块对应的次数范围（使用整数）
        const rangeSize = (globalMaxCount - globalMinCount) / colorBlockCount;
        
        // 格式化范围显示（始终显示为整数）
        function formatRange(min, max, isLast, index) {
            // 将范围边界取整
            // 第一个范围从最小值开始，其他范围从上一个范围的结束值+1开始
            const minInt = index === 0 ? Math.floor(globalMinCount) : Math.floor(min) + 1;
            const maxInt = isLast ? Math.floor(globalMaxCount) : Math.floor(max);
            
            // 如果最小值和最大值相同，只显示一个值
            if (minInt === maxInt) {
                return `${minInt}`;
            }
            
            return `${minInt}-${maxInt}`;
        }
        
        // 创建颜色块
        for (let i = 0; i < colorBlockCount; i++) {
            // 创建包装容器
            const wrapper = document.createElement('div');
            wrapper.classList.add('color-block-wrapper');
            
            // 创建颜色块
            const colorBlock = document.createElement('div');
            colorBlock.classList.add('color-block');
            
            // 计算当前颜色块对应的次数值（使用区间中点）
            const countValue = globalMinCount + (i + 0.5) * rangeSize;
            
            // 计算颜色
            const color = calculateColor(globalMinCount, globalMaxCount, countValue);
            colorBlock.style.backgroundColor = `rgb(${color.r}, ${color.g}, ${color.b})`;
            
            // 存储次数范围信息（用于筛选，保持精度）
            const minRange = globalMinCount + i * rangeSize;
            // 最后一个颜色块应该包含最大值
            const maxRange = (i === colorBlockCount - 1) ? globalMaxCount + 0.1 : globalMinCount + (i + 1) * rangeSize;
            colorBlock.dataset.minRange = minRange;
            colorBlock.dataset.maxRange = maxRange;
            colorBlock.dataset.index = i;
            
            // 添加点击事件
            colorBlock.addEventListener('click', handleColorBarClick);
            
            // 创建范围标签
            const label = document.createElement('div');
            label.classList.add('color-block-label');
            label.textContent = formatRange(minRange, maxRange, i === colorBlockCount - 1, i);
            
            // 将颜色块和标签添加到包装容器
            wrapper.appendChild(colorBlock);
            wrapper.appendChild(label);
            
            // 将包装容器添加到颜色横条
            colorFilterBar.appendChild(wrapper);
        }
    }
    
    /**
     * 处理颜色横条点击事件
     */
    function handleColorBarClick(event) {
        const colorBlock = event.target;
        const minRange = parseFloat(colorBlock.dataset.minRange);
        const maxRange = parseFloat(colorBlock.dataset.maxRange);
        const index = parseInt(colorBlock.dataset.index);
        
        // 更新选中状态
        if (selectedColorRange && selectedColorRange.index === index) {
            // 如果点击的是已选中的颜色块，则取消筛选
            resetFilter();
            return;
        }
        
        // 移除所有颜色块的选中状态
        document.querySelectorAll('.color-block').forEach(block => {
            block.classList.remove('selected');
        });
        
        // 添加当前颜色块的选中状态
        colorBlock.classList.add('selected');
        selectedColorRange = { minRange, maxRange, index };
        
        // 筛选IP单元格
        filterIPCells(minRange, maxRange);
    }
    
    /**
     * 根据次数范围筛选IP单元格
     */
    function filterIPCells(minRange, maxRange) {
        const allCells = document.querySelectorAll('.ip-table td');
        
        allCells.forEach(cell => {
            // 移除之前的筛选类
            cell.classList.remove('filtered-out', 'filtered-in');
            
            // 跳过非坊内IP和0次IP
            if (cell.classList.contains('non-fang') || cell.classList.contains('count-zero')) {
                return;
            }
            
            // 获取IP的次数
            const count = parseInt(cell.getAttribute('data-count')) || 0;
            
            // 判断是否在范围内
            if (count >= minRange && count < maxRange) {
                // 在范围内：高亮显示
                cell.classList.add('filtered-in');
            } else {
                // 不在范围内：变暗
                cell.classList.add('filtered-out');
            }
        });
    }
    
    /**
     * 重置筛选，显示所有IP
     */
    function resetFilter() {
        // 移除所有颜色块的选中状态
        document.querySelectorAll('.color-block').forEach(block => {
            block.classList.remove('selected');
        });
        
        // 移除所有IP单元格的筛选类
        document.querySelectorAll('.ip-table td').forEach(cell => {
            cell.classList.remove('filtered-out', 'filtered-in');
        });
        
        selectedColorRange = null;
    }
    
    // 页面加载完成后应用热力图颜色
    document.addEventListener('DOMContentLoaded', function() {
        applyHeatmapColors();
        
        // 绑定重置按钮点击事件
        const resetBtn = document.getElementById('resetFilterBtn');
        if (resetBtn) {
            resetBtn.addEventListener('click', resetFilter);
        }
    });
    
    // 自动刷新：每60秒刷新一次页面以获取最新数据
    setInterval(function() {
        location.reload();
    }, 60000); // 60000毫秒 = 60秒 = 1分钟
</script>
</html>
