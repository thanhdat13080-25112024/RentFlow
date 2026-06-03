const TRANSLATIONS = {
    vi: {
        appName: 'Quản Lý Trọ', dataMonth: 'Tháng',
        tabs: { dashboard: 'Tổng quan', rooms: 'Phòng & Khách', bills: 'Hóa đơn', revenue: 'Doanh thu', settings: 'Cài đặt' },
        status_map: { unpaid: 'Chưa thu', paid: 'Đã thu', prepaid: 'Đóng trước', empty: 'Trống' },
        statTotalRooms:'Tổng phòng', statOccupied:'đang thuê', statEmpty:'trống', statRooms:'phòng',
        statUnpaid:'Chưa thu', statPaid:'Đã thu', statPrepaid:'Đóng trước',
        statCollected:'Đã thu tháng này', statDeposit:'Tiền cọc giữ', statThisMonth:'tháng này', statPrevMonths:'tháng trước',
        chartTitle:'Doanh thu 6 tháng gần nhất', chartSubtitle:'Tổng: điện + dịch vụ + tiền phòng',
        donutTitle:'Trạng thái',
        attentionTitle:'⚠ Phòng cần chú ý', activityTitle:'Hoạt động gần đây',
        dashUnpaidNote:'phòng chưa thu tiền tháng này.', dashAllPaid:'Tất cả đã thu! 🎉',
        actPaid:'đã thanh toán', actPrepaid:'đóng tiền trước',
        viewAll:'Xem tất cả', noActivity:'Chưa có hoạt động',
        filterAll:'Tất cả', filterUnpaid:'Chưa thu', filterPaid:'Đã thu', filterPrepaid:'Đóng trước',
        room:'Phòng', tenant:'Khách thuê', total:'Tổng', status:'Trạng thái', period:'Kỳ',
        electricity:'Số điện', oldReading:'Số cũ', newReading:'Số mới', usage:'Sử dụng',
        breakdown:'Chi tiết tháng này', rentFee:'Tiền phòng', serviceFee:'Phí dịch vụ',
        electricityFee:'Tiền điện', totalAmount:'Tổng cộng', month:'Tháng',
        markPaid:'✓ Đánh dấu đã thu', prepaid:'📅 Đóng trước nhiều tháng',
        qrBtn:'QR / Hóa đơn', edit:'Chỉnh sửa', history:'Lịch sử',
        deposit:'Tiền cọc', moveIn:'Ngày thuê:', back:'Quay lại',
        selectRoom:'Chọn phòng để xem chi tiết', noBills:'Không có hóa đơn nào',
        noElecInput:'⚠ Chưa nhập số điện tháng này',
        floor:'Tầng', roomsSubtitle:'phòng', vacantRoom:'Chưa có khách',
        collect:'✓ Thu', remind:'Nhắc',
        revenueTitle:'Tổng hợp doanh thu', revMonth:'Tháng/Năm', noRevData:'Chưa có dữ liệu doanh thu',
        settingsTitle:'Cài đặt hệ thống',
        settingLabels: { electricity_unit_price:'Giá điện (VNĐ/kWh)', bank_account:'Số tài khoản', bank_name:'Ngân hàng', account_holder:'Chủ tài khoản' },
        editRoom:'Chỉnh sửa thông tin phòng', saveChanges:'Lưu thay đổi',
        rentFee:'Tiền phòng', serviceFee:'Dịch vụ', depositLabel:'Tiền cọc',
        moveInDate:'Ngày thuê', initialReading:'Số điện ban đầu', contactInfo:'Khách thuê & Liên hệ',
        invoiceTitle:'HÓA ĐƠN TIỀN TRỌ', transferContent:'Nội dung chuyển khoản',
        downloadInvoice:'Tải ảnh hóa đơn', close:'Đóng cửa sổ',
        historyTitle:'Lịch sử phòng', historySubtitle:'Toàn bộ thông tin qua các tháng', noHistory:'Chưa có dữ liệu',
        prepaidTitle:'Đóng tiền trước', prepaidHint:'Nhập các tháng đóng trước cho phòng',
        confirm:'Xác nhận', cancel:'Hủy',
        search:'Tìm phòng, khách, SĐT...',
        viewFloor:'Dạng tầng', viewList:'Dạng cột',
        importCSV:'Import CSV',
        greeting_morning:'Chào buổi sáng', greeting_afternoon:'Chào buổi chiều', greeting_evening:'Chào buổi tối',
        settingOk:'Đã lưu cài đặt!', confirmCollect:'Thu tiền phòng',
        quick:'Thao tác', logout:'Đăng xuất',
        actionMarkPaid:'Đánh dấu đã thu phòng...', actionViewQR:'Xem QR phòng...', actionUpdateElec:'Cập nhật số điện', actionCancel:'Hủy',
    },
    en: {
        appName:'Rent Manager', dataMonth:'Month',
        tabs:{ dashboard:'Overview', rooms:'Rooms & Tenants', bills:'Bills', revenue:'Revenue', settings:'Settings' },
        status_map:{ unpaid:'Unpaid', paid:'Paid', prepaid:'Prepaid', empty:'Vacant' },
        statTotalRooms:'Total Rooms', statOccupied:'occupied', statEmpty:'vacant', statRooms:'rooms',
        statUnpaid:'Unpaid', statPaid:'Paid', statPrepaid:'Prepaid',
        statCollected:'Collected This Month', statDeposit:'Deposits Held', statThisMonth:'this month', statPrevMonths:'prev months',
        chartTitle:'Revenue — Last 6 Months', chartSubtitle:'Electricity + service + rent',
        donutTitle:'Status',
        attentionTitle:'⚠ Needs Attention', activityTitle:'Recent Activity',
        dashUnpaidNote:'rooms unpaid this month.', dashAllPaid:'All collected! 🎉',
        actPaid:'paid', actPrepaid:'prepaid months',
        viewAll:'View all', noActivity:'No recent activity',
        filterAll:'All', filterUnpaid:'Unpaid', filterPaid:'Paid', filterPrepaid:'Prepaid',
        room:'Room', tenant:'Tenant', total:'Total', status:'Status', period:'Period',
        electricity:'Electricity', oldReading:'Old Reading', newReading:'New Reading', usage:'Usage',
        breakdown:'This Month Breakdown', rentFee:'Rent', serviceFee:'Service Fee',
        electricityFee:'Electricity', totalAmount:'Total', month:'Month',
        markPaid:'✓ Mark as Paid', prepaid:'📅 Prepaid Months',
        qrBtn:'QR / Invoice', edit:'Edit', history:'History',
        deposit:'Deposit', moveIn:'Move-in:', back:'Back',
        selectRoom:'Select a room to view details', noBills:'No bills found',
        noElecInput:'⚠ No meter reading entered',
        floor:'Floor', roomsSubtitle:'rooms', vacantRoom:'Vacant',
        collect:'✓ Collect', remind:'Remind',
        revenueTitle:'Revenue Report', revMonth:'Month/Year', noRevData:'No revenue data yet',
        settingsTitle:'System Settings',
        settingLabels:{ electricity_unit_price:'Electricity Rate (VND/kWh)', bank_account:'Bank Account', bank_name:'Bank', account_holder:'Account Holder' },
        editRoom:'Edit Room Info', saveChanges:'Save Changes',
        rentFee:'Rent', serviceFee:'Service', depositLabel:'Deposit',
        moveInDate:'Move-in Date', initialReading:'Initial Reading', contactInfo:'Tenant & Contact',
        invoiceTitle:'RENT INVOICE', transferContent:'Transfer Reference',
        downloadInvoice:'Download Invoice', close:'Close',
        historyTitle:'Room History', historySubtitle:'All billing records', noHistory:'No records',
        prepaidTitle:'Mark Prepaid', prepaidHint:'Enter months to mark prepaid for room',
        confirm:'Confirm', cancel:'Cancel',
        search:'Search rooms, tenants...',
        viewFloor:'Floor View', viewList:'List View',
        importCSV:'Import CSV',
        greeting_morning:'Good morning', greeting_afternoon:'Good afternoon', greeting_evening:'Good evening',
        settingOk:'Settings saved!', confirmCollect:'Collect payment',
        quick:'Quick', logout:'Sign out',
        actionMarkPaid:'Mark room as paid...', actionViewQR:'View QR code...', actionUpdateElec:'Update meter reading', actionCancel:'Cancel',
    },
    ko: {
        appName:'임대 관리', dataMonth:'월',
        tabs:{ dashboard:'개요', rooms:'방 & 세입자', bills:'청구서', revenue:'수익', settings:'설정' },
        status_map:{ unpaid:'미수금', paid:'수납완료', prepaid:'선납', empty:'공실' },
        statTotalRooms:'총 방 수', statOccupied:'입주', statEmpty:'공실', statRooms:'개',
        statUnpaid:'미수금', statPaid:'수납완료', statPrepaid:'선납',
        statCollected:'이번 달 수납', statDeposit:'보증금', statThisMonth:'이번 달', statPrevMonths:'이전 달',
        chartTitle:'최근 6개월 수익', chartSubtitle:'전기 + 관리비 + 임대료',
        donutTitle:'현황',
        attentionTitle:'⚠ 주의 필요', activityTitle:'최근 활동',
        dashUnpaidNote:'개 방 미수금.', dashAllPaid:'전부 수납완료! 🎉',
        actPaid:'납부', actPrepaid:'선납',
        viewAll:'전체 보기', noActivity:'최근 활동 없음',
        filterAll:'전체', filterUnpaid:'미수금', filterPaid:'수납완료', filterPrepaid:'선납',
        room:'방', tenant:'세입자', total:'합계', status:'상태', period:'기간',
        electricity:'전기', oldReading:'이전 검침', newReading:'현재 검침', usage:'사용량',
        breakdown:'이번 달 내역', rentFee:'임대료', serviceFee:'관리비',
        electricityFee:'전기요금', totalAmount:'합계', month:'월',
        markPaid:'✓ 수납 완료', prepaid:'📅 선납 처리',
        qrBtn:'QR / 영수증', edit:'편집', history:'이력',
        deposit:'보증금', moveIn:'입주일:', back:'뒤로',
        selectRoom:'방을 선택하세요', noBills:'청구서 없음',
        noElecInput:'⚠ 전기 검침 미입력',
        floor:'층', roomsSubtitle:'개 방', vacantRoom:'공실',
        collect:'✓ 수납', remind:'알림',
        revenueTitle:'수익 보고서', revMonth:'월/연', noRevData:'수익 데이터 없음',
        settingsTitle:'시스템 설정',
        settingLabels:{ electricity_unit_price:'전기 요금(VND/kWh)', bank_account:'계좌번호', bank_name:'은행', account_holder:'예금주' },
        editRoom:'방 정보 편집', saveChanges:'저장',
        rentFee:'임대료', serviceFee:'관리비', depositLabel:'보증금',
        moveInDate:'입주일', initialReading:'초기 검침', contactInfo:'세입자 & 연락처',
        invoiceTitle:'임대 청구서', transferContent:'이체 내용',
        downloadInvoice:'청구서 다운로드', close:'닫기',
        historyTitle:'방 이력', historySubtitle:'전체 납부 기록', noHistory:'기록 없음',
        prepaidTitle:'선납 처리', prepaidHint:'선납 월 입력 (방',
        confirm:'확인', cancel:'취소',
        search:'방, 세입자 검색...',
        viewFloor:'층별 보기', viewList:'목록 보기',
        importCSV:'CSV 가져오기',
        greeting_morning:'좋은 아침', greeting_afternoon:'안녕하세요', greeting_evening:'좋은 저녁',
        settingOk:'설정 저장 완료!', confirmCollect:'수납 처리',
        quick:'빠른 작업', logout:'로그아웃',
        actionMarkPaid:'수납 완료 처리...', actionViewQR:'QR 코드 보기...', actionUpdateElec:'전기 검침 입력', actionCancel:'취소',
    },
    ja: {
        appName:'賃貸管理', dataMonth:'月',
        tabs:{ dashboard:'概要', rooms:'部屋 & 入居者', bills:'請求書', revenue:'収益', settings:'設定' },
        status_map:{ unpaid:'未収', paid:'収納済', prepaid:'前払', empty:'空室' },
        statTotalRooms:'総部屋数', statOccupied:'入居中', statEmpty:'空室', statRooms:'室',
        statUnpaid:'未収', statPaid:'収納済', statPrepaid:'前払',
        statCollected:'今月収納', statDeposit:'預り敷金', statThisMonth:'今月', statPrevMonths:'前月',
        chartTitle:'直近6ヶ月収益', chartSubtitle:'電気 + 管理費 + 家賃',
        donutTitle:'状況',
        attentionTitle:'⚠ 要注意', activityTitle:'最近の活動',
        dashUnpaidNote:'室未収。', dashAllPaid:'全部収納済! 🎉',
        actPaid:'納付', actPrepaid:'前払',
        viewAll:'全て表示', noActivity:'活動なし',
        filterAll:'全て', filterUnpaid:'未収', filterPaid:'収納済', filterPrepaid:'前払',
        room:'部屋', tenant:'入居者', total:'合計', status:'状態', period:'期間',
        electricity:'電気', oldReading:'前回検針', newReading:'今回検針', usage:'使用量',
        breakdown:'今月内訳', rentFee:'家賃', serviceFee:'管理費',
        electricityFee:'電気代', totalAmount:'合計', month:'月',
        markPaid:'✓ 収納済にする', prepaid:'📅 前払処理',
        qrBtn:'QR / 領収書', edit:'編集', history:'履歴',
        deposit:'敷金', moveIn:'入居日:', back:'戻る',
        selectRoom:'部屋を選択', noBills:'請求書なし',
        noElecInput:'⚠ 検針未入力',
        floor:'階', roomsSubtitle:'室', vacantRoom:'空室',
        collect:'✓ 収納', remind:'通知',
        revenueTitle:'収益レポート', revMonth:'月/年', noRevData:'収益データなし',
        settingsTitle:'システム設定',
        settingLabels:{ electricity_unit_price:'電気料金(VND/kWh)', bank_account:'口座番号', bank_name:'銀行', account_holder:'口座名義' },
        editRoom:'部屋情報編集', saveChanges:'保存',
        rentFee:'家賃', serviceFee:'管理費', depositLabel:'敷金',
        moveInDate:'入居日', initialReading:'初回検針', contactInfo:'入居者 & 連絡先',
        invoiceTitle:'賃貸請求書', transferContent:'振込内容',
        downloadInvoice:'請求書ダウンロード', close:'閉じる',
        historyTitle:'部屋履歴', historySubtitle:'全納付記録', noHistory:'記録なし',
        prepaidTitle:'前払処理', prepaidHint:'前払月を入力 (部屋',
        confirm:'確認', cancel:'キャンセル',
        search:'部屋・入居者検索...',
        viewFloor:'階層表示', viewList:'リスト表示',
        importCSV:'CSVインポート',
        greeting_morning:'おはようございます', greeting_afternoon:'こんにちは', greeting_evening:'こんばんは',
        settingOk:'設定を保存しました!', confirmCollect:'収納処理',
        quick:'クイック', logout:'ログアウト',
        actionMarkPaid:'収納済にする...', actionViewQR:'QRコード表示...', actionUpdateElec:'検針入力', actionCancel:'キャンセル',
    },
    zh: {
        appName:'租金管理', dataMonth:'月',
        tabs:{ dashboard:'概览', rooms:'房间 & 租户', bills:'账单', revenue:'收入', settings:'设置' },
        status_map:{ unpaid:'未收款', paid:'已收款', prepaid:'预付款', empty:'空置' },
        statTotalRooms:'总房间数', statOccupied:'已入住', statEmpty:'空置', statRooms:'间',
        statUnpaid:'未收款', statPaid:'已收款', statPrepaid:'预付款',
        statCollected:'本月已收', statDeposit:'押金总额', statThisMonth:'本月', statPrevMonths:'上月',
        chartTitle:'近6个月收入', chartSubtitle:'电费 + 服务费 + 房租',
        donutTitle:'状态',
        attentionTitle:'⚠ 需关注', activityTitle:'最近活动',
        dashUnpaidNote:'间未收款。', dashAllPaid:'全部收款! 🎉',
        actPaid:'已付款', actPrepaid:'预付',
        viewAll:'查看全部', noActivity:'暂无活动',
        filterAll:'全部', filterUnpaid:'未收款', filterPaid:'已收款', filterPrepaid:'预付款',
        room:'房间', tenant:'租户', total:'合计', status:'状态', period:'期间',
        electricity:'用电', oldReading:'上期读数', newReading:'本期读数', usage:'用量',
        breakdown:'本月明细', rentFee:'房租', serviceFee:'服务费',
        electricityFee:'电费', totalAmount:'合计', month:'月',
        markPaid:'✓ 标记已收款', prepaid:'📅 预付处理',
        qrBtn:'QR / 账单', edit:'编辑', history:'历史',
        deposit:'押金', moveIn:'入住:', back:'返回',
        selectRoom:'请选择房间查看详情', noBills:'暂无账单',
        noElecInput:'⚠ 未录入电表读数',
        floor:'楼', roomsSubtitle:'间房', vacantRoom:'空置',
        collect:'✓ 收款', remind:'提醒',
        revenueTitle:'收入报告', revMonth:'月/年', noRevData:'暂无收入数据',
        settingsTitle:'系统设置',
        settingLabels:{ electricity_unit_price:'电费单价(VND/kWh)', bank_account:'银行账号', bank_name:'银行', account_holder:'账户名' },
        editRoom:'编辑房间信息', saveChanges:'保存',
        rentFee:'房租', serviceFee:'服务费', depositLabel:'押金',
        moveInDate:'入住日期', initialReading:'初始读数', contactInfo:'租户 & 联系方式',
        invoiceTitle:'租金账单', transferContent:'转账备注',
        downloadInvoice:'下载账单', close:'关闭',
        historyTitle:'房间历史', historySubtitle:'全部账单记录', noHistory:'暂无记录',
        prepaidTitle:'预付处理', prepaidHint:'输入预付月份 (房间',
        confirm:'确认', cancel:'取消',
        search:'搜索房间、租户...',
        viewFloor:'楼层视图', viewList:'列表视图',
        importCSV:'导入CSV',
        greeting_morning:'早上好', greeting_afternoon:'下午好', greeting_evening:'晚上好',
        settingOk:'设置已保存!', confirmCollect:'收款处理',
        quick:'快捷操作', logout:'退出登录',
        actionMarkPaid:'标记已收款...', actionViewQR:'查看QR码...', actionUpdateElec:'更新电表读数', actionCancel:'取消',
    }
};

function app(initialMonth, initialYear) {
    return {
        month: initialMonth,
        year: initialYear,
        lang: localStorage.getItem('qlTroLang') || 'vi',
        activeTab: 'dashboard',
        billTab: 'all',
        searchQuery: '',
        selectedBillId: null,
        roomView: 'floor',
        isMobile: false,

        bills: [],
        rooms: [],
        settings: {},
        revenueSummary: [],
        revenueExpanded: false,

        toast: { show: false, message: '', type: 'success' },
        editRoomModal: { show: false, room: {} },
        roomHistory: { show: false, room_number: '', records: [] },
        qrModal: { show: false, room: '', amount: 0, room_id: 0, rent_fee: 0, service_fee: 0, elec_fee: 0, elec_usage: 0 },
        confirmModal: { show: false, title: '', message: '', callback: null },
        prepaidModal: { show: false, room_id: 0, room_number: '', months: '' },

        langFlags: { vi:'🇻🇳', en:'🇺🇸', ko:'🇰🇷', ja:'🇯🇵', zh:'🇨🇳' },
        langNames: { vi:'Tiếng Việt', en:'English', ko:'한국어', ja:'日本語', zh:'中文' },

        get t() { return TRANSLATIONS[this.lang]; },

        get tabs() {
            return [
                { id: 'dashboard', label: this.t.tabs.dashboard },
                { id: 'rooms',     label: this.t.tabs.rooms },
                { id: 'settings',  label: this.t.tabs.settings },
            ];
        },
        get mobileTabs() {
            return [
                { id: 'dashboard', label: this.t.tabs.dashboard, icon: 'fas fa-chart-pie' },
                { id: 'rooms',     label: this.t.tabs.rooms,     icon: 'fas fa-door-open' },
                { id: 'settings',  label: this.t.tabs.settings,  icon: 'fas fa-sliders' },
            ];
        },

        get selectedBill() {
            if (!this.selectedBillId) return null;
            return this.bills.find(b => b.room_id === this.selectedBillId) || null;
        },

        get filteredBills() {
            let list = this.bills.filter(b => b.is_occupied);
            if (this.billTab !== 'all') list = list.filter(b => b.status === this.billTab);
            if (this.searchQuery) {
                const q = this.searchQuery.toLowerCase();
                list = list.filter(b =>
                    (b.room_number || '').toLowerCase().includes(q) ||
                    (b.contact_info || '').toLowerCase().includes(q)
                );
            }
            return list;
        },

        get stats() {
            const occupied = this.bills.filter(b => b.is_occupied);
            const paidBills = occupied.filter(b => b.status === 'paid' || b.status === 'prepaid');
            return {
                totalRooms: this.rooms.length,
                occupiedCount: this.rooms.filter(r => r.is_occupied).length,
                emptyCount: this.rooms.filter(r => !r.is_occupied).length,
                unpaidCount: occupied.filter(b => b.status === 'unpaid').length,
                paidCount: occupied.filter(b => b.status === 'paid').length,
                prepaidCount: occupied.filter(b => b.status === 'prepaid').length,
                collectedAmount: paidBills.reduce((s, b) => s + (b.total || 0), 0),
                depositTotal: this.rooms.filter(r => r.is_occupied).reduce((s, r) => s + (r.deposit || 0), 0),
            };
        },

        get attentionRooms() {
            return this.bills.filter(b => b.status === 'unpaid' && b.is_occupied).slice(0, 3);
        },

        get recentActivity() {
            return this.bills
                .filter(b => (b.status === 'paid' || b.status === 'prepaid') && b.paid_at)
                .sort((a, b) => new Date(b.paid_at) - new Date(a.paid_at))
                .map(b => ({ room: b.room_number, type: b.status, amount: b.total, when: this.relativeTime(b.paid_at) }))
                .slice(0, 5);
        },

        get dashboardChart() {
            // Build a fixed 6-slot window (5 months ago → current month).
            // Slots without real data get zero so the chart always shows 6 bars.
            const slots = [];
            for (let i = 5; i >= 0; i--) {
                let m = this.month - i;
                let y = this.year;
                if (m <= 0) { m += 12; y--; }
                slots.push({ month: m, year: y });
            }
            const rows = slots.map(s => {
                const found = this.revenueSummary.find(
                    r => r.month === s.month && r.year === s.year
                );
                return { month: s.month, year: s.year, total_revenue: found ? found.total_revenue : 0 };
            });
            if (!rows.some(r => r.total_revenue > 0)) return [];
            const max = Math.max(...rows.map(r => r.total_revenue), 1);
            return rows.map(r => ({
                label: 'T' + r.month,
                v: r.total_revenue,
                pct: Math.round((r.total_revenue / max) * 90),
                current: r.month === this.month && r.year === this.year
            }));
        },

        get revChartData() {
            const recent = [...this.revenueSummary].slice(-12);
            if (!recent.length) return [];
            const max = Math.max(...recent.map(r => r.total_revenue), 1);
            return recent.map(r => ({
                label: 'T' + r.month,
                v: r.total_revenue,
                pct: Math.round((r.total_revenue / max) * 90),
                current: r.month === this.month && r.year === this.year
            }));
        },

        get donut() {
            const occupied = this.bills.filter(b => b.is_occupied);
            const total = occupied.length || 1;
            const paidCount = occupied.filter(b => b.status === 'paid').length;
            const prepaidCount = occupied.filter(b => b.status === 'prepaid').length;
            const unpaidCount = occupied.filter(b => b.status === 'unpaid').length;
            const paid = parseFloat((paidCount / total * 100).toFixed(2));
            const prepaid = parseFloat((prepaidCount / total * 100).toFixed(2));
            const unpaid = parseFloat((unpaidCount / total * 100).toFixed(2));
            return {
                paid, prepaid, unpaid,
                paidOffset: 0,
                prepaidOffset: paid,
                unpaidOffset: paid + prepaid,
                paidCount, prepaidCount, unpaidCount,
                paidPct: Math.round((paidCount + prepaidCount) / total * 100)
            };
        },

        get floorGroups() {
            const floorMap = {};
            let filtered = this.rooms;
            if (this.searchQuery) {
                const q = this.searchQuery.toLowerCase();
                filtered = this.rooms.filter(r =>
                    (r.room_number || '').toLowerCase().includes(q) ||
                    (r.contact_info || '').toLowerCase().includes(q)
                );
            }
            filtered.forEach(r => {
                const fl = (r.room_number || '?')[0];
                if (!floorMap[fl]) floorMap[fl] = [];
                floorMap[fl].push(r);
            });
            return Object.keys(floorMap).sort().map(fl => ({
                num: fl,
                rooms: floorMap[fl],
                total: floorMap[fl].length,
                occupied: floorMap[fl].filter(r => r.is_occupied).length
            }));
        },

        async init() {
            this.isMobile = window.innerWidth < 768;
            window.addEventListener('resize', () => { this.isMobile = window.innerWidth < 768; });
            await Promise.all([this.loadData(), this.loadSettings(), this.loadRooms()]);
            this.loadRevenueSummary();
            this.initLiquidLight();
        },

        initLiquidLight() {
            if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
            if (!window.matchMedia('(hover: hover)').matches) return;

            document.addEventListener('mousemove', (e) => {
                const targets = document.querySelectorAll('.lg-surface-regular');
                targets.forEach(el => {
                    const rect = el.getBoundingClientRect();
                    const x = ((e.clientX - rect.left) / rect.width) * 100;
                    const y = ((e.clientY - rect.top) / rect.height) * 100;
                    el.style.setProperty('--lg-light-x', `${x}%`);
                    el.style.setProperty('--lg-light-y', `${y}%`);
                });
            }, { passive: true });
        },

        setLang(l) { this.lang = l; localStorage.setItem('qlTroLang', l); },

        getGreeting() {
            const h = new Date().getHours();
            if (h < 12) return this.t.greeting_morning;
            if (h < 18) return this.t.greeting_afternoon;
            return this.t.greeting_evening;
        },

        todayStr() {
            const localeMap = { vi: 'vi-VN', en: 'en-US', ko: 'ko-KR', ja: 'ja-JP', zh: 'zh-CN' };
            return new Date().toLocaleDateString(localeMap[this.lang] || 'vi-VN', { weekday: 'long', day: '2-digit', month: '2-digit', year: 'numeric' });
        },

        relativeTime(ts) {
            if (!ts) return '';
            const diff = (Date.now() - new Date(ts)) / 3600000;
            if (diff < 1) return '< 1h';
            if (diff < 24) return Math.round(diff) + 'h';
            return Math.round(diff / 24) + 'd';
        },

        showToast(msg, type = 'success') {
            this.toast = { show: true, message: msg, type };
            setTimeout(() => { this.toast.show = false; }, 3000);
        },

        async loadData() {
            const res = await fetch(`/api/bills?month=${this.month}&year=${this.year}`);
            if (res.status === 401) return;
            this.bills = await res.json();
            if (this.selectedBillId && !this.bills.find(b => b.room_id === this.selectedBillId))
                this.selectedBillId = null;
        },

        async loadRooms() {
            const res = await fetch('/api/rooms');
            if (res.status === 401) return;
            this.rooms = await res.json();
        },

        async loadSettings() {
            const res = await fetch('/api/settings');
            if (res.status === 401) return;
            this.settings = await res.json();
        },

        async loadRevenueSummary() {
            const res = await fetch('/api/bills/revenue/summary');
            if (res.status === 401) return;
            this.revenueSummary = (await res.json()).reverse();
        },

        getBillForRoom(room) {
            return this.bills.find(b => b.room_id === room.id) || null;
        },

        async handleImport(event) {
            const file = event.target.files[0];
            if (!file) return;
            const formData = new FormData();
            formData.append('file', file);
            try {
                this.showToast('Đang import...');
                const res = await fetch('/api/bills/import-csv', { method: 'POST', body: formData });
                const result = await res.json();
                if (res.ok) {
                    this.showToast(result.message);
                    await this.loadData();
                    this.loadRevenueSummary();
                } else {
                    this.showToast(result.detail || 'Lỗi import', 'error');
                }
            } catch (e) {
                this.showToast('Lỗi kết nối server', 'error');
            } finally {
                event.target.value = '';
            }
        },

        async saveSettings() {
            const data = Object.keys(this.settings).map(key => ({ key, value: this.settings[key] }));
            await fetch('/api/settings', { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(data) });
            this.showToast(this.t.settingOk || 'Đã lưu cài đặt!');
            this.loadData();
        },

        async openEditModal(bill) {
            const room = this.rooms.find(r => r.id === bill.room_id);
            if (room) {
                this.editRoomModal.room = {
                    ...room,
                    rent_price: bill.rent_fee,
                    service_fee: bill.service_fee,
                    deposit: bill.deposit,
                    contact_info: bill.contact_info,
                    move_in_date: bill.move_in_date,
                    old_reading: bill.old_reading
                };
                this.editRoomModal.show = true;
            }
        },

        async openRoomEdit(room) {
            const bill = this.getBillForRoom(room);
            if (bill) {
                await this.openEditModal(bill);
            } else {
                this.editRoomModal.room = { ...room };
                this.editRoomModal.show = true;
            }
        },

        async saveQuickEdit() {
            const room = this.editRoomModal.room;
            const res = await fetch('/api/rooms/update', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ ...room, month: this.month, year: this.year })
            });
            if (res.ok) {
                this.showToast(`Đã cập nhật phòng ${room.room_number}`);
                this.editRoomModal.show = false;
                await this.loadData();
                await this.loadRooms();
            }
        },

        async showHistory(room) {
            const res = await fetch(`/api/rooms/${room.id}/history`);
            this.roomHistory.records = await res.json();
            this.roomHistory.room_number = room.room_number;
            this.editRoomModal.show = false;
            this.roomHistory.show = true;
        },

        async updateElectricity(bill) {
            await fetch('/api/electricity', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ room_id: bill.room_id, month: this.month, year: this.year, new_reading: bill.new_reading })
            });
            this.showToast(`Đã lưu số điện P.${bill.room_number}`);
            await this.loadData();
        },

        async updateElectricityByRoom(room, newReading) {
            const bill = this.getBillForRoom(room);
            if (!bill) return;
            bill.new_reading = parseInt(newReading) || 0;
            await this.updateElectricity(bill);
        },

        async toggleStatus(bill) {
            if (bill.status === 'unpaid') {
                this.quickCollect(bill);
            } else if (bill.status === 'paid') {
                this.prepaidModal = { show: true, room_id: bill.room_id, room_number: bill.room_number, months: '' };
            }
        },

        async quickCollect(bill) {
            this.confirmModal = {
                show: true,
                title: this.t.confirmCollect || 'Thu tiền phòng',
                message: `Xác nhận phòng ${bill.room_number} đã đóng đủ tiền tháng ${this.month}?`,
                callback: async () => {
                    await fetch('/api/bills/mark-paid', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ room_id: bill.room_id, month: this.month, year: this.year })
                    });
                    this.showToast(`Đã thu tiền phòng ${bill.room_number}`);
                    await this.loadData();
                }
            };
        },

        async confirmPrepaid() {
            if (!this.prepaidModal.months) return;
            await fetch('/api/bills/mark-prepaid', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    room_id: this.prepaidModal.room_id,
                    months: this.prepaidModal.months.split(',').map(m => parseInt(m.trim())).filter(Boolean),
                    year: this.year
                })
            });
            this.prepaidModal.show = false;
            this.showToast('Đã lưu đóng tiền trước!');
            await this.loadData();
        },

        showQR(bill) {
            if (!bill) return;
            this.qrModal = {
                show: true,
                room: bill.room_number,
                room_id: bill.room_id,
                amount: bill.total || 0,
                rent_fee: bill.rent_fee || 0,
                service_fee: bill.service_fee || 0,
                elec_fee: bill.electricity_fee || 0,
                elec_usage: bill.is_fixed ? 0 : ((bill.new_reading || 0) - (bill.old_reading || 0))
            };
        },

        getQRUrl() {
            const bank = this.settings.bank_name || 'MB';
            const account = this.settings.bank_account || '';
            const desc = encodeURIComponent(`PHONG ${this.qrModal.room} THANG ${this.month}`);
            return `https://qr.sepay.vn/img?bank=${bank}&acc=${account}&template=compact&amount=${this.qrModal.amount}&des=${desc}`;
        },

        async saveInvoiceAsImage() {
            const element = document.getElementById('invoice-content');
            this.showToast('Đang tạo ảnh hóa đơn...');
            try {
                const canvas = await html2canvas(element, { useCORS: true, scale: 2, backgroundColor: '#ffffff', logging: false });
                const link = document.createElement('a');
                link.download = `HoaDon_Phong${this.qrModal.room}_Thang${this.month}.png`;
                link.href = canvas.toDataURL('image/png', 1.0);
                link.click();
                this.showToast('Ảnh đã được tải về!');
            } catch (e) {
                this.showToast('Lỗi khi tạo ảnh!', 'error');
            }
        },

        prevMonth() {
            if (this.month === 1) { this.month = 12; this.year--; } else { this.month--; }
            this.updateUrl(); this.loadData();
        },

        nextMonth() {
            const now = new Date();
            let maxM = now.getMonth() + 2, maxY = now.getFullYear();
            if (maxM > 12) { maxM = 1; maxY++; }
            if (this.year > maxY || (this.year === maxY && this.month >= maxM)) {
                this.showToast(`Tối đa đến tháng ${maxM}/${maxY}`); return;
            }
            if (this.month === 12) { this.month = 1; this.year++; } else { this.month++; }
            this.updateUrl(); this.loadData();
        },

        updateUrl() {
            const url = new URL(window.location);
            url.searchParams.set('month', this.month);
            url.searchParams.set('year', this.year);
            window.history.pushState({}, '', url);
        },

        handleKeydown(e) {
            if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
            if (e.key === 'ArrowLeft') this.prevMonth();
            if (e.key === 'ArrowRight') this.nextMonth();
        },

        getFloorBg(roomNumber) {
            const f = (roomNumber || '?')[0];
            return {
                '1': 'bg-violet-600',
                '2': 'bg-indigo-600',
                '3': 'bg-cyan-600',
                '4': 'bg-violet-500',
                '5': 'bg-indigo-500',
                '6': 'bg-cyan-500',
                '7': 'bg-violet-700',
            }[f] || 'bg-gray-500';
        },

        getFloorText(roomNumber) {
            const f = (roomNumber || '?')[0];
            return {
                '1': 'text-violet-600',
                '2': 'text-indigo-600',
                '3': 'text-cyan-600',
                '4': 'text-violet-500',
                '5': 'text-indigo-500',
                '6': 'text-cyan-500',
                '7': 'text-violet-700',
            }[f] || 'text-gray-500';
        },

        getFloorBorder(roomNumber) {
            const f = (roomNumber || '?')[0];
            return {
                '1': 'border-violet-600',
                '2': 'border-indigo-600',
                '3': 'border-cyan-600',
                '4': 'border-violet-500',
                '5': 'border-indigo-500',
                '6': 'border-cyan-500',
                '7': 'border-violet-700',
            }[f] || 'border-gray-500';
        },

        formatMoney(amount) { return new Intl.NumberFormat('vi-VN').format(amount || 0) + 'đ'; },

        formatInput(val) {
            if (val === null || val === undefined || val === '') return '';
            return val.toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.');
        },

        parseInput(val) { return parseInt((val || '').toString().replace(/\./g, '')) || 0; },

        formatDate(val) {
            if (!val) return '';
            let v = val.replace(/\D/g, '').slice(0, 8);
            if (v.length > 4) return v.slice(0,2) + '/' + v.slice(2,4) + '/' + v.slice(4);
            if (v.length > 2) return v.slice(0,2) + '/' + v.slice(2);
            return v;
        },

        displayDate(dateStr) {
            if (!dateStr) return '';
            const parts = dateStr.split('-');
            if (parts.length !== 3) return dateStr;
            return `${parts[2]}/${parts[1]}/${parts[0]}`;
        },

        fixDate(room) {
            if (!room.move_in_date) return;
            let v = room.move_in_date.replace(/\D/g, '');
            if (v.length === 6) room.move_in_date = v.slice(0,2) + '/' + v.slice(2,4) + '/20' + v.slice(4);
        },

        fixMoney(room, field) {
            if (room[field] > 0 && room[field] < 10000) room[field] = room[field] * 1000;
        },

        async logout() {
            const res = await fetch('/api/auth/logout', { method: 'POST' });
            if (res.ok) window.location.href = '/login';
        }
    };
}
