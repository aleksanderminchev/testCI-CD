import { Helmet } from 'react-helmet-async';
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
// @mui
import {
  Tab,
  Tabs,
  Card,
  Table,
  Button,
  Tooltip,
  Divider,
  TableBody,
  Container,
  IconButton,
  TableContainer,
} from '@mui/material';
// routes
import { PATH_DASHBOARD } from '../../../../routes/paths';
// @types
import { IStudent } from '../../../../@types/student';
// components
import Iconify from '../../../../components/iconify';
import Scrollbar from '../../../../components/scrollbar';
import ConfirmDialog from '../../../../components/confirm-dialog';
import { useSettingsContext } from '../../../../components/settings';
import {
  useTable,
  getComparator,
  emptyRows,
  TableNoData,
  TableEmptyRows,
  TableHeadCustom,
  TableSelectedAction,
  TablePaginationCustom,
} from '../../../../components/table';
// sections
import StudentTableToolbar from './StudentTableToolbar';
import StudentTableRow from './StudentTableRow';

// ----------------------------------------------------------------------

const STATUS_OPTIONS = ['active', 'inactive', 'all'];

const TYPE_OPTIONS = ['all', 'independent', 'child'];

const TABLE_HEAD = [
  { id: 'name', label: 'Navn', align: 'left' },
  { id: 'email', label: 'Email', align: 'left' },
  { id: 'phone', label: 'Telefon', align: 'left' },
  { id: 'student_type', label: 'Type', align: 'left' },
  { id: 'status', label: 'Status', align: 'left' },
  { id: '' },
];
const TABLE_HEAD_NON_ADMIN = [
  { id: 'name', label: 'Navn', align: 'left' },
  { id: 'email', label: 'Email', align: 'left' },
  { id: 'phone', label: 'Telefon', align: 'left' },
  { id: '' },
];
// ----------------------------------------------------------------------
type Props = {
  students: IStudent[];
  isAdmin: boolean;
};
export default function StudentList({ students, isAdmin }: Props) {
  const {
    dense,
    page,
    order,
    orderBy,
    rowsPerPage,
    setPage,
    //
    selected,
    setSelected,
    onSelectRow,
    onSelectAllRows,
    //
    onSort,
    onChangeDense,
    onChangePage,
    onChangeRowsPerPage,
  } = useTable();

  const { themeStretch } = useSettingsContext();

  const navigate = useNavigate();

  const [tableData, setTableData] = useState<IStudent[]>([]);

  const [filterName, setFilterName] = useState('');

  const [filterType, setFilterType] = useState('all');

  const [openConfirm, setOpenConfirm] = useState(false);

  const [filterStatus, setFilterStatus] = useState('active');

  useEffect(() => {
    console.log(students);
    if (students.length) {
      setTableData(students);
    }
  }, [students]);

  const dataFiltered = applyFilter({
    inputData: tableData,
    comparator: getComparator(order, orderBy),
    filterName,
    filterStatus,
    filterType,
  });

  const dataInPage = dataFiltered.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage);

  const denseHeight = dense ? 52 : 72;

  const isFiltered = filterName !== '' || filterType !== 'all' || filterStatus !== 'all';

  const isNotFound =
    (!dataFiltered.length && !!filterName) ||
    (!dataFiltered.length && !!filterType) ||
    (!dataFiltered.length && !!filterStatus);

  const handleOpenConfirm = () => {
    setOpenConfirm(true);
  };

  const handleCloseConfirm = () => {
    setOpenConfirm(false);
  };

  const handleFilterStatus = (event: React.SyntheticEvent<Element, Event>, newValue: string) => {
    setPage(0);
    setFilterStatus(newValue);
  };

  const handleFilterName = (event: React.ChangeEvent<HTMLInputElement>) => {
    setPage(0);
    setFilterName(event.target.value);
  };

  const handleFilterType = (event: React.ChangeEvent<HTMLInputElement>) => {
    setPage(0);
    setFilterType(event.target.value);
  };

  const handleDeleteRow = (id: string) => {
    const deleteRow = tableData.filter((row) => row.id !== id);
    setSelected([]);
    setTableData(deleteRow);

    if (page > 0) {
      if (dataInPage.length < 2) {
        setPage(page - 1);
      }
    }
  };

  const handleDeleteRows = (selectedRows: string[]) => {
    const deleteRows = tableData.filter((row) => !selectedRows.includes(row.id));
    setSelected([]);
    setTableData(deleteRows);

    if (page > 0) {
      if (selectedRows.length === dataInPage.length) {
        setPage(page - 1);
      } else if (selectedRows.length === dataFiltered.length) {
        setPage(0);
      } else if (selectedRows.length > dataInPage.length) {
        const newPage = Math.ceil((tableData.length - selectedRows.length) / rowsPerPage) - 1;
        setPage(newPage);
      }
    }
  };
  console.log(tableData);
  const handleEditRow = (id: string) => {
    navigate(PATH_DASHBOARD.student.profile(id));
  };

  const handleResetFilter = () => {
    setFilterName('');
    setFilterType('all');
    setFilterStatus('all');
  };

  return (
    <>
      <Helmet>
        <title>Elever</title>
      </Helmet>

      <Container maxWidth={themeStretch ? false : 'lg'}>
        <Card>
          {isAdmin ? (
            <>
              <Tabs
                value={filterStatus}
                onChange={handleFilterStatus}
                sx={{
                  px: 2,
                  bgcolor: 'background.neutral',
                }}
              >
                {STATUS_OPTIONS.map((tab) => (
                  <Tab key={tab} label={tab} value={tab} />
                ))}
              </Tabs>
              <Divider />
              <StudentTableToolbar
                isFiltered={isFiltered}
                filterName={filterName}
                filterType={filterType}
                optionsType={TYPE_OPTIONS}
                onFilterName={handleFilterName}
                onFilterType={handleFilterType}
                onResetFilter={handleResetFilter}
              />
            </>
          ) : (
            <>
              <Divider />
              <StudentTableToolbar
                isFiltered={isFiltered}
                filterName={filterName}
                filterType={filterType}
                optionsType={TYPE_OPTIONS}
                onFilterName={handleFilterName}
                onFilterType={handleFilterType}
                onResetFilter={handleResetFilter}
              />
            </>
          )}

          <TableContainer sx={{ position: 'relative', overflow: 'unset' }}>
            {isAdmin ? (
              <TableSelectedAction
                dense={dense}
                numSelected={selected.length}
                rowCount={tableData.length}
                onSelectAllRows={(checked) =>
                  onSelectAllRows(
                    checked,
                    tableData.map((row) => row.id)
                  )
                }
                action={
                  <Tooltip title="Delete">
                    <IconButton color="primary" onClick={handleOpenConfirm}>
                      <Iconify icon="eva:trash-2-outline" />
                    </IconButton>
                  </Tooltip>
                }
              />
            ) : (
              <></>
            )}

            <Scrollbar>
              <Table size={dense ? 'small' : 'medium'} sx={{ minWidth: 800 }}>
                {isAdmin ? (
                  <TableHeadCustom
                    order={order}
                    orderBy={orderBy}
                    headLabel={TABLE_HEAD}
                    rowCount={tableData.length}
                    numSelected={selected.length}
                    onSort={onSort}
                    onSelectAllRows={(checked) =>
                      onSelectAllRows(
                        checked,
                        tableData.map((row) => row.id)
                      )
                    }
                  />
                ) : (
                  <TableHeadCustom
                    order={order}
                    orderBy={orderBy}
                    headLabel={TABLE_HEAD_NON_ADMIN}
                    rowCount={tableData.length}
                    numSelected={selected.length}
                    onSort={onSort}
                    onSelectAllRows={(checked) =>
                      onSelectAllRows(
                        checked,
                        tableData.map((row) => row.id)
                      )
                    }
                  />
                )}

                <TableBody>
                  {dataFiltered
                    .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                    .map((row) => (
                      <StudentTableRow
                        isAdmin={isAdmin}
                        key={row.id}
                        row={row}
                        selected={selected.includes(row.id)}
                        onSelectRow={() => onSelectRow(row.id)}
                        onDeleteRow={() => handleDeleteRow(row.id)}
                        onEditRow={() => handleEditRow(row.id)}
                      />
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
            //
            dense={dense}
            onChangeDense={onChangeDense}
          />
        </Card>
      </Container>

      <ConfirmDialog
        open={openConfirm}
        onClose={handleCloseConfirm}
        title="Delete"
        content={
          <>
            Are you sure want to delete <strong> {selected.length} </strong> items?
          </>
        }
        action={
          <Button
            variant="contained"
            color="error"
            onClick={() => {
              handleDeleteRows(selected);
              handleCloseConfirm();
            }}
          >
            Delete
          </Button>
        }
      />
    </>
  );
}

// ----------------------------------------------------------------------

function applyFilter({
  inputData,
  comparator,
  filterName,
  filterStatus,
  filterType,
}: {
  inputData: IStudent[];
  comparator: (a: any, b: any) => number;
  filterName: string;
  filterStatus: string;
  filterType: string;
}) {
  const stabilizedThis = inputData.map((el, index) => [el, index] as const);

  stabilizedThis.sort((a, b) => {
    const order = comparator(a[0], b[0]);
    if (order !== 0) return order;
    return a[1] - b[1];
  });

  inputData = stabilizedThis.map((el) => el[0]);

  if (filterName) {
    inputData = inputData.filter((student) => {
      const info = `${student.first_name} ${student.last_name} ${student.email} ${student.phone}`;
      return info.toLowerCase().indexOf(filterName.toLowerCase()) !== -1;
    });
  }

  if (filterStatus !== 'all') {
    inputData = inputData.filter((student) => student.status === filterStatus);
  }

  if (filterType !== 'all') {
    inputData = inputData.filter((student) => student.student_type === filterType);
  }

  return inputData;
}
