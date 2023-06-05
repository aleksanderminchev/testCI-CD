import orderBy from 'lodash/orderBy';
import { EventInput } from '@fullcalendar/core';
import { useState } from 'react';
// @mui
import { DatePicker } from '@mui/x-date-pickers';
import {
  Box,
  Stack,
  Drawer,
  Divider,
  Tooltip,
  TextField,
  Typography,
  IconButton,
  ListItemText,
  ListItemButton,
  Switch,
  Autocomplete,
  TextFieldProps,
} from '@mui/material';
// @types
import { IStudent } from '../../../@types/student';
import { ITutor } from '../../../@types/tutor';
import { ICustomer } from '../../../@types/customer';
// utils
import { fDateTime } from '../../../utils/formatTime';
// components
import Iconify from '../../../components/iconify';
import Scrollbar from '../../../components/scrollbar';
import { ColorMultiPicker } from '../../../components/color-utils';

// ----------------------------------------------------------------------

type Props = {
  admin: boolean;
  openFilter: boolean;
  teachers: ITutor[];
  students: IStudent[];
  customers: ICustomer[];
  filterStudents: { value: IStudent; priority: string }[];
  filterTeachers: { value: ITutor; priority: string }[];
  filterCustomers: { value: ICustomer; priority: string }[];
  filterByPaid: boolean;
  filterByTrial: boolean;
  events: EventInput[];
  onResetFilter: VoidFunction;
  onCloseFilter: VoidFunction;
  colorOptions: string[];
  filterEventColor: string[];
  startDate: Date | null;
  endDate: Date | null;
  setStartDate: (value: Date | null) => void;
  setEndDate: (value: Date | null) => void;
  onSelectEvent: (eventId: string) => void;
  onFilterEventColor: (eventColor: string) => void;
  onFilterEventTeacher: (options: { value: ITutor; priority: string }[]) => void;
  onFilterEventStudent: (options: { value: IStudent; priority: string }[]) => void;
  onFilterEventCustomer: (options: { value: ICustomer; priority: string }[]) => void;
  onFilterPaidLessons: (option: boolean) => void;
  onFilterTrialLessons: (option: boolean) => void;
};

export default function CalendarFilterDrawer({
  admin,
  teachers,
  students,
  customers,
  filterStudents,
  filterTeachers,
  filterCustomers,
  filterByPaid,
  filterByTrial,
  events,
  startDate,
  endDate,
  setStartDate,
  setEndDate,
  openFilter,
  colorOptions,
  onCloseFilter,
  onResetFilter,
  onSelectEvent,
  filterEventColor,
  onFilterEventColor,
  onFilterEventStudent,
  onFilterEventTeacher,
  onFilterPaidLessons,
  onFilterEventCustomer,
  onFilterTrialLessons,
}: Props) {
  /**
   * This function sorts an array of teachers based on priority.
   *
   * @function sortArrayTeachers
   * @param {ITutor[]} teachersArray - The array of teachers to be sorted.
   * @returns {Array<{ value: ITutor; priority: string }>} A sorted array of teachers with priority info.
   */
  const sortArrayTeachers = (teachersArray: ITutor[]) => {
    const priorityArray = teachersArray.map((value) => {
      const priority = filterStudents.find((student) =>
        value.students.includes(student.value.id.toString())
      );
      return { value, priority: priority ? 'Priority' : 'All' };
    });
    return priorityArray.sort((a, b) => {
      if (a.priority === 'Priority') {
        return -1;
      }
      return 1;
    });
  };

  /**
   * This function sorts an array of students based on priority.
   *
   * @function sortArrayStudents
   * @param {IStudent[]} studentsArray - The array of students to be sorted.
   * @returns {Array<{ value: IStudent; priority: string }>} A sorted array of students with priority info.
   */
  const sortArrayStudents = (studentsArray: IStudent[]) => {
    const priorityArray = studentsArray.map((value) => {
      const priority = filterTeachers.find((teacher) =>
        value.teachers.includes(teacher.value.id.toString())
      );
      const customerPriority = filterCustomers.find((customer) =>
        customer.value.students.includes(value.id.toString())
      );
      return { value, priority: priority || customerPriority ? 'Priority' : 'All' };
    });

    return priorityArray.sort((a, b) => {
      if (a.priority === 'Priority') {
        return -1;
      }
      return 1;
    });
  };

  /**
   * This function sorts an array of customers based on priority.
   *
   * @function sortArrayCustomers
   * @param {ICustomer[]} customersArray - The array of customers to be sorted.
   * @returns {Array<{ value: ICustomer; priority: string }>} A sorted array of customers with priority info.
   */
  const sortArrayCustomers = (customersArray: ICustomer[]) => {
    const priorityArray = customersArray.map((value) => {
      const priority = filterStudents.find((student) =>
        value.students.includes(student.value.id.toString())
      );
      return { value, priority: priority ? 'Priority' : 'All' };
    });

    return priorityArray.sort((a, b) => {
      if (a.priority === 'Priority') {
        return -1;
      }
      return 1;
    });
  };
  return (
    <Drawer
      anchor="right"
      open={openFilter}
      onClose={onCloseFilter}
      BackdropProps={{
        invisible: true,
      }}
      PaperProps={{
        sx: { width: 320 },
      }}
    >
      <Stack
        direction="row"
        alignItems="center"
        justifyContent="space-between"
        sx={{ pl: 2, pr: 1, py: 2 }}
      >
        <Typography variant="subtitle1">Filters</Typography>

        <Tooltip title="Reset">
          <Box sx={{ position: 'relative' }}>
            <IconButton onClick={onResetFilter}>
              <Iconify icon="ic:round-refresh" />
            </IconButton>

            <Box
              sx={{
                top: 6,
                right: 4,
                width: 8,
                height: 8,
                borderRadius: '50%',
                position: 'absolute',
                bgcolor: 'error.main',
              }}
            />
          </Box>
        </Tooltip>
      </Stack>

      <Divider />

      <Typography
        variant="caption"
        sx={{
          color: 'text.secondary',
          fontWeight: 'fontWeightMedium',
          p: (theme) => theme.spacing(2, 2, 1, 2),
        }}
      >
        Attendance
      </Typography>

      <ColorMultiPicker
        colorOptionsText={['Attended', 'Scheduled', 'Cancelled']}
        colors={colorOptions}
        selected={filterEventColor}
        onChangeColor={onFilterEventColor}
        translate="yes"
        sx={{ mx: 2 }}
      />
      <Typography
        variant="caption"
        sx={{
          color: 'text.secondary',
          fontWeight: 'fontWeightMedium',
          p: (theme) => theme.spacing(2, 2, 1, 2),
        }}
      >
        Filter by paid lessons
      </Typography>

      <Switch
        defaultChecked={false}
        checked={filterByPaid}
        onChange={(e) => onFilterPaidLessons(!filterByPaid)}
        inputProps={{ 'aria-label': 'controlled' }}
      />
      <Typography
        variant="caption"
        sx={{
          color: 'text.secondary',
          fontWeight: 'fontWeightMedium',
          p: (theme) => theme.spacing(2, 2, 1, 2),
        }}
      >
        Filter by trial lessons
      </Typography>

      <Switch
        defaultChecked={false}
        checked={filterByTrial}
        onChange={(e) => onFilterTrialLessons(!filterByTrial)}
        inputProps={{ 'aria-label': 'controlled' }}
      />
      <Typography
        variant="caption"
        sx={{
          p: 2,
          color: 'text.secondary',
          fontWeight: 'fontWeightMedium',
        }}
      >
        Range
      </Typography>

      <Stack spacing={2} sx={{ px: 2 }}>
        <DatePicker
          label="Starttidspunkt"
          value={startDate}
          onChange={setStartDate}
          renderInput={(params) => <TextField disabled size="small" {...params} />}
          InputProps={{}}
        />

        <DatePicker
          label="Sluttidspunkt"
          value={endDate}
          onChange={setEndDate}
          renderInput={(params) => <TextField size="small" disabled {...params} />}
        />
        <Autocomplete
          onChange={(event, value) => onFilterEventTeacher(value)}
          multiple
          value={filterTeachers}
          options={sortArrayTeachers([...teachers])}
          groupBy={(option) => option.priority}
          getOptionLabel={(option: { value: ITutor; priority: string }) =>
            `${option.value.first_name} ${option.value.last_name}`
          }
          filterSelectedOptions
          renderInput={(params: JSX.IntrinsicAttributes & TextFieldProps) => (
            <TextField {...params} label="Filter Teachers" placeholder="Teachers" />
          )}
        />
        <Autocomplete
          onChange={(event, value) => onFilterEventStudent(value)}
          multiple
          value={filterStudents}
          groupBy={(option) => option.priority}
          options={sortArrayStudents([...students])}
          getOptionLabel={(option: { value: IStudent; priority: string }) =>
            `${option.value.first_name} ${option.value.last_name}`
          }
          filterSelectedOptions
          renderInput={(params: JSX.IntrinsicAttributes & TextFieldProps) => (
            <TextField {...params} label="Filter Students" placeholder="Students" />
          )}
        />
        <Autocomplete
          onChange={(event, value) => onFilterEventCustomer(value)}
          multiple
          value={filterCustomers}
          groupBy={(option) => option.priority}
          options={sortArrayCustomers([...customers])}
          getOptionLabel={(option: { value: ICustomer; priority: string }) =>
            `${option.value.first_name} ${option.value.last_name}`
          }
          filterSelectedOptions
          renderInput={(params: JSX.IntrinsicAttributes & TextFieldProps) => (
            <TextField {...params} label="Filter by customers" placeholder="Customers" />
          )}
        />
      </Stack>
      <Typography
        variant="caption"
        sx={{
          p: 2,
          color: 'text.secondary',
          fontWeight: 'fontWeightMedium',
        }}
      >
        Events ({events.length})
      </Typography>

      <Scrollbar sx={{ height: 1 }}>
        {orderBy(events, ['end'], ['desc']).map((event) => (
          <ListItemButton
            key={event.id}
            onClick={() => {
              console.log(event);
              onSelectEvent(event.id as string);
            }}
            sx={{ py: 1.5, borderBottom: (theme) => `dashed 1px ${theme.palette.divider}` }}
          >
            <Box
              sx={{
                top: 16,
                left: 0,
                width: 0,
                height: 0,
                position: 'absolute',
                borderRight: '10px solid transparent',
                borderTop: `10px solid ${event.color}`,
              }}
            />

            <ListItemText
              disableTypography
              primary={
                <Typography variant="subtitle2" sx={{ fontSize: 13, mt: 0.5 }}>
                  {event.title}
                </Typography>
              }
              secondary={
                <Typography
                  variant="caption"
                  component="div"
                  sx={{ fontSize: 11, color: 'text.disabled' }}
                >
                  {event.allDay ? (
                    fDateTime(event.start as Date, 'dd MMM yy HH:mm')
                  ) : (
                    <>
                      {`${fDateTime(event.start as Date, 'dd MMM yy HH:mm')} - ${fDateTime(
                        event.end as Date,
                        'dd MMM yy HH:mm'
                      )}`}
                    </>
                  )}
                </Typography>
              }
              sx={{ display: 'flex', flexDirection: 'column-reverse' }}
            />
          </ListItemButton>
        ))}
      </Scrollbar>
    </Drawer>
  );
}
