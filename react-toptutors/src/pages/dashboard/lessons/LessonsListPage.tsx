import { Helmet } from 'react-helmet-async';

import { useEffect, useState } from 'react';

// @mui
import {
  Tab,
  Tabs,
  Card,
  Table,
  Divider,
  TableBody,
  Container,
  TableContainer,
} from '@mui/material';
// routes
import { PATH_DASHBOARD } from '../../../routes/paths';
// @types
import { ILesson } from '../../../@types/lesson';
// components
import Scrollbar from '../../../components/scrollbar';

import CustomBreadcrumbs from '../../../components/custom-breadcrumbs';
import { useSettingsContext } from '../../../components/settings';
import {
  useTable,
  getComparator,
  emptyRows,
  TableNoData,
  TableEmptyRows,
  TableHeadCustom,
  TablePaginationCustom,
} from '../../../components/table';
// redux
import { useDispatch, useSelector } from '../../../redux/store';
import { getLessons } from '../../../redux/slices/lesson';
// sections
import { LessonsTableRow } from '../../../sections/@dashboard/lessons';
import { fTimestamp } from '../../../utils/formatTime';
import SelectPeriode from '../../../sections/@dashboard/lessons/SelectPeriode';
import ResetButton from '../../../sections/@dashboard/lessons/ResetButton';

// ----------------------------------------------------------------------
const PAID_OPTIONS = ['all', 'unpaid', 'paid'];

const TABLE_HEAD = [
  { id: 'student', label: 'Elev' },
  { id: 'date', label: 'Dato' },
  { id: 'startTime', label: 'Starttidspunkt' },
  { id: 'endTime', label: 'Sluttidspunkt' },
  { id: 'status', label: 'Status' },
  { id: 'duration', label: 'Varighed' },
  { id: 'wages', label: 'Løn' },
  { id: 'paid', label: 'Udbetalt' },
];

// ----------------------------------------------------------------------

export default function LessonsListPage() {
  const {
    dense,
    page,
    order,
    orderBy,
    rowsPerPage,
    setPage,
    onSort,
    onChangeDense,
    onChangePage,
    onChangeRowsPerPage,
  } = useTable();

  const { themeStretch } = useSettingsContext();
  const dispatch = useDispatch();
  const [tableData, setTableData] = useState<ILesson[]>([]);
  const { lessons } = useSelector((state) => state.lesson);
  const [filterStudent] = useState('');

  const [filterPaid, setFilterPaid] = useState('all');
  const [endDate, setEndDate] = useState<Date | null>(null);

  const [startDate, setStartDate] = useState<Date | null>(null);
  useEffect(() => {
    if (!lessons.length) {
      dispatch(getLessons());
    }
  }, [dispatch, lessons.length]);

  useEffect(() => {
    setTableData(lessons);
  }, [lessons]);

  const dataFiltered = applyFilter({
    inputData: tableData,
    comparator: getComparator(order, orderBy),
    filterPaid,
    filterStartDate: startDate,
    filterEndDate: endDate,
  });

  const denseHeight = dense ? 52 : 72;

  const isFiltered = filterStudent !== '' || filterPaid !== 'all';

  const isNotFound =
    (!dataFiltered.length && !!filterStudent) || (!dataFiltered.length && !!filterPaid);

  const handleFilterPaid = (event: React.SyntheticEvent<Element, Event>, newValue: string) => {
    setPage(0);
    setFilterPaid(newValue);
  };

  const handleResetFilter = () => {
    setFilterPaid('all');
  };

  const [selectedLessonId, setSelectedLessonId] = useState<string | null>(null);

  const handleResetDates = () => {
    setStartDate(null);
    setEndDate(null);
  };

  return (
    <>
      <Helmet>
        <title> Lektioner</title>
      </Helmet>

      <Container maxWidth={themeStretch ? false : 'lg'}>
        <CustomBreadcrumbs
          heading="Lektioner"
          links={[
            { name: 'Oversigt', href: PATH_DASHBOARD.root },
            { name: 'Lektioner', href: PATH_DASHBOARD.lesson.root },
            { name: 'List' },
          ]}
        />

        <Card>
          <Tabs
            value={filterPaid}
            onChange={handleFilterPaid}
            sx={{
              px: 2,
              bgcolor: 'background.neutral',
            }}
          >
            {PAID_OPTIONS.map((tab) => (
              <Tab key={tab} label={tab} value={tab} />
            ))}

            <ResetButton onResetFilter={handleResetFilter} isFiltered={isFiltered} />
          </Tabs>

          <SelectPeriode
            lessons={tableData}
            startDate={startDate}
            endDate={endDate}
            onSelectLesson={(lessonId) => {
              if (lessonId) {
                setSelectedLessonId(lessonId);
              }
            }}
            setStartDate={(value) => {
              setStartDate(value);
            }}
            setEndDate={(value) => {
              setEndDate(value);
            }}
            onResetFilter={handleResetDates}
          />

          <Divider />

          <TableContainer sx={{ position: 'relative', overflow: 'unset' }}>
            <Scrollbar>
              <Table size={dense ? 'small' : 'medium'} sx={{ minWidth: 800 }}>
                <TableHeadCustom
                  order={order}
                  orderBy={orderBy}
                  headLabel={TABLE_HEAD}
                  rowCount={tableData.length}
                  onSort={onSort}
                />

                <TableBody>
                  {dataFiltered
                    .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                    .map((row) => (
                      <LessonsTableRow key={row.id} row={row} />
                    ))}

                  <TableEmptyRows
                    height={denseHeight}
                    emptyRows={emptyRows(page, rowsPerPage, tableData.length)}
                  />

                  <TableNoData isNotFound={isNotFound} />
                </TableBody>
              </Table>
            </Scrollbar>
          </TableContainer>

          <TablePaginationCustom
            count={dataFiltered.length}
            page={page}
            rowsPerPage={rowsPerPage}
            onPageChange={onChangePage}
            onRowsPerPageChange={onChangeRowsPerPage}
            dense={dense}
            onChangeDense={onChangeDense}
          />
        </Card>
      </Container>
    </>
  );
}

// ----------------------------------------------------------------------

function applyFilter({
  inputData,
  comparator,
  filterPaid,
  filterStartDate,
  filterEndDate,
}: {
  inputData: ILesson[];
  comparator: (a: any, b: any) => number;
  filterPaid: string;
  filterStartDate: Date | null;
  filterEndDate: Date | null;
}) {
  const stabilizedThis = inputData.map((el, index) => [el, index] as const);

  stabilizedThis.sort((a, b) => {
    const order = comparator(a[0], b[0]);
    if (order !== 0) return order;
    return a[1] - b[1];
  });

  inputData = stabilizedThis.map((el) => el[0]);

  if (filterPaid !== 'all') {
    inputData = inputData.filter((lesson) => (filterPaid === 'paid' ? lesson.paid : !lesson.paid));
  }

  if (filterStartDate && filterEndDate) {
    inputData = inputData.filter(
      (lesson: ILesson) =>
        fTimestamp(lesson.from_time) >= fTimestamp(filterStartDate) &&
        fTimestamp(lesson.from_time) <= fTimestamp(filterEndDate)
    );
  }

  return inputData;
}
