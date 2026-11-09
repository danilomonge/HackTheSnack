package de.pecus.api.util;

import java.sql.Time;
import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.time.LocalDate;
import java.time.LocalTime;
import java.time.ZoneId;
import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;
import java.time.temporal.ChronoUnit;
import java.util.Calendar;
import java.util.Date;
import java.util.GregorianCalendar;
import java.util.Locale;
import java.util.TimeZone;

import javax.xml.datatype.DatatypeConstants;
import javax.xml.datatype.DatatypeFactory;
import javax.xml.datatype.XMLGregorianCalendar;

import org.apache.commons.lang3.time.FastDateFormat;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import de.pecus.api.constant.GeneralConstants;

public class DateTimeUtil {
	
	/**
	 * Logger
	 */
	private static final Logger LOGGER = LoggerFactory.getLogger(DateTimeUtil.class);

	private static final SimpleDateFormat sdfDatetimeISO8601 = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss+00:00");
	private static final SimpleDateFormat sdfDatetime = new SimpleDateFormat("yyyy-MM-dd hh:mm:ss a");
	private static final SimpleDateFormat sdfDatetime24 = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
	private static final SimpleDateFormat sdfTime = new SimpleDateFormat("hh:mm a");
	private static final SimpleDateFormat sdfTime24 = new SimpleDateFormat("HH:mm");
	private static final SimpleDateFormat sdfDate = new SimpleDateFormat("yyyy-MM-dd");
	private static final SimpleDateFormat sdfFactura = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss");
	private static final SimpleDateFormat sdfFolio = new SimpleDateFormat("yyyyMMdd");
	private static final SimpleDateFormat sdfDiaLetraSmsNotificacion = new SimpleDateFormat("EEEE", new Locale("es", "MX"));
	private static final SimpleDateFormat sdfDiaNumericoSmsNotificacion = new SimpleDateFormat("dd");
	private static final SimpleDateFormat sdfMesSmsNotificacion = new SimpleDateFormat("MMMM", new Locale("es", "MX"));
	private static final SimpleDateFormat sdfAnioSmsNotificacion = new SimpleDateFormat("yyyy");
	private static final SimpleDateFormat sdfMobile = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ssXXX");
	private static final SimpleDateFormat sdfRequestDate = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss.SSSXXX");
	private static final String sdfUTCFormat = "dd-MM-yyyy HH:mm:ss";
	private static final String patternTime = "hh:mm a";
	private static final String patternTime24 = "HH:mm";
	private static final SimpleDateFormat sdfDatetime24H = new SimpleDateFormat("yyyy-MM-dd HH:mm");
	private static final SimpleDateFormat sdfDatetime12H = new SimpleDateFormat("dd-MM-yyyy hh:mm a");
	private static final TimeZone UTC_TIME_ZONE = TimeZone.getTimeZone("UTC");
	private static final SimpleDateFormat sdfDateTimeZoned = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss");
	private static final SimpleDateFormat sdfDatetimeT24H = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm");
	private static final Locale localeMobile = new Locale.Builder().setLanguage("es").setRegion("ES").build();
	private static final SimpleDateFormat sdfMobileFormat = new SimpleDateFormat("dd 'de' MMMM 'de' yyyy", localeMobile);
	private static final SimpleDateFormat sdfSeparateDiagonal = new SimpleDateFormat("dd/MM/yyyy");
	
	/**
	 * Convierte un objeto String a uno del tipo Time de java.sql
	 * 
	 * @param String en formato "hh:mm a"
	 * @return java.sql.time
	 **/
	public static Time stringToTime(String string) { //TODO - Sin cambios
		try {
			Time time = new Time(sdfTime.parse(string).getTime());
			return time;
		} catch (Exception ex) {
			return null;
		}
	}	
	
	/**
	 * Convierte un objeto Date a un String
	 * 
	 * @param Date con la fecha ingresada
	 * @return String en formato "hh:mm a"
	 **/
	public static String dateToStringTime(Date date) { //TODO - Correccion de javadoc
		
		String rValue =  null;
		
		try {
			
			rValue =   sdfTime.format(date);	
			
		} catch (Exception ex) {
			rValue = null;
		}
		return rValue;
	}
	
	/**
	 * Convierte un objeto Date a un String
	 * 
	 * @param Date con la fecha ingresada
	 * @return String en formato "HH:mm" (24 hrs) 
	 **/
	public static String dateToStringTime24(Date date) { // TODO - Correccion de javadoc
		
		String rValue =  null;
		
		try {
			
			rValue =   sdfTime24.format(date);	
			
		} catch (Exception ex) {
			rValue = null;
		}
		return rValue;
	}
	

	/**
	 * Convierte un objeto String a uno del tipo Time de java.sql en formato 24 horas
	 * 
	 * @param string en formato "HH:mm"
	 * @return java.sql.time
	 **/
	public static Time stringToTime24(String string) { // Sin cambios
		try {
			return new Time(sdfTime24.parse(string).getTime());
		} catch (Exception ex) {
			return null;
		}
	}
	
	/**
	 * Convierte un objeto Time a uno del tipo String formato 24 horas
	 * 
	 * @return string en formato "HH:mm"
	 * @param java.sql.time
	 **/
	public static String timeToString24(Time time) { // TODO - Sin cambios
		try {
			LocalTime l = LocalTime.parse(time.toString());
			l.format(DateTimeFormatter.ofPattern(patternTime24));
			return l.format(DateTimeFormatter.ofPattern(patternTime24));
		} catch (Exception ex) {
			return null;
		}
	}
	
	/**
	 * Convierte un objeto java.sql.Time a uno del tipo String
	 * 
	 * @return string con la fecha en formato "hh:mm AM/PM"
	 * @param java sql.time
	 **/
	public static String timeToString(Time time) { // TODO - Sin cambios
		try {
			LocalTime l = LocalTime.parse(time.toString());
			l.format(DateTimeFormatter.ofPattern(patternTime));
			return l.format(DateTimeFormatter.ofPattern(patternTime));
		} catch (Exception ex) {
			return null;
		}
	}

	/**
	 * Convierte un objeto String a uno del tipo Date
	 * 
	 * @param String en formato "yyyy-MM-dd"
	 * @return Date con la fecha a convertir
	 **/
	public static Date stringToDate(String date) { // TODO - Correccion en javadoc
		try {
			return sdfDate.parse(date);
		} catch (Exception ex) {
			return null;
		}
	}

	/**
	 * Convierte un objeto Date a uno del tipo String en formato "yyyy-MM-dd"
	 * 
	 * @param Date con la fecha ingresada
	 * @return String formato "yyyy-MM-dd"
	 **/
	public static String dateToString(Date date) { // TODO - Correccion menor javadoc
		try {
			return sdfDate.format(date);
		} catch (Exception ex) {
			return null;
		}
	}

	
	/**
	 * Convierte un objeto Date a uno del tipo String en formato "yyyy-MM-dd
	 * hh:mm:ss a"
	 * 
	 * @param Date con la fecha a convertir
	 * @return String formato "yyyy-MM-dd hh:mm:ss a"
	 **/
	public static String datetimeToString(Date datetime) { //TODO - Cambio menor 
		try {
			return sdfDatetime.format(datetime);
		} catch (Exception ex) {
			return null;
		}
	}
	
	
	
	/**
	 * Convierte un objeto Date a uno del tipo String en formato "yyyy-MM-dd
	 * hh:mm a"
	 * 
	 * @param Date con la fecha a convertir
	 * @return String formato "yyyy-MM-dd hh:mm a"
	 **/
	public static String datetimeToString12h(Date datetime) { // TODO - Cambio menor
		try {
			return sdfDatetime12H.format(datetime);
		} catch (Exception ex) {
			return null;
		}
	}	
	
	/**
	 * Convierte un objeto Date a uno del tipo String en formato "yyyy-MM-dd"
	 * 
	 * @param Date con la fecha a convertir
	 * @return string formato "yyyy-MM-dd"
	 **/
	public static String dateToStringComplete(Date datetime) { //TODO - cambio en string de retorno
		try {
			return sdfDate.format(datetime);
		} catch (Exception ex) {
			return null;
		}
	}
	
	
	/**
	 * Convierte un objeto String en formato "yyyy-MM-dd HH:mm" a uno del tipo Date
	 * 
	 * @param String formato "yyyy-MM-dd HH:mm"
	 * @return Date con la fecha a convertir
	 **/
	public static Date stringToDatetime24(String datetime) { //TODO - Sin cambios
		try {
			return sdfDatetime24H.parse(datetime);
		} catch (Exception ex) {
			return null;
		}
	}
	
	/**
	 * Convierte un objeto Date a un String en formato "yyyy-MM-dd HH:mm" 
	 * 
	 * @param date Fecha a convertir
	 * @return String con formato "yyyy-MM-dd HH:mm" 
	 **/
	public static String dateTimeToString24(Date date) { // TODO - Sin cambios
		try {
			return sdfDatetime24H.format(date);
		} catch (Exception ex) {
			return null;
		}
	}
	
	
	/**
	 * Convierte un objeto Date a uno del tipo String en formato ISO 8601
	 *
	 * @param Date con la fecha a convertir
	 * @return String formato "yyyy-MM-dd'T'HH:mm:ss+00:00"
	 **/
	public static String datetimeToStringISO8601(Date date) { //TODO - sin cambios
		try {
			return sdfDatetimeISO8601.format(date);
		} catch (Exception ex) {
			return null;
		}
	}
	
	/**
	 * Convierte un objeto String en formato "yyyy-MM-dd HH:mm:ss" a uno del tipo Date
	 * 
	 * @param String formato "yyyy-MM-dd HH:mm:ss"
	 * @return Date con la fecha a convertir
	 **/
	public static Date stringToDatetime24H(String datetime) { // TODO - Sin cambios
		try {
			return sdfDatetime24.parse(datetime);
		} catch (Exception ex) {
			return null;
		}
	}
	
	/**
	 * Convierte un objeto Date a uno del tipo String en formato "yyyy-MM-dd
	 * HH:mm:ss"
	 * 
	 * @param Date con la fecha a convertir
	 * @return String formato "yyyy-MM-dd HH:mm:ss"
	 **/
	public static String datetime24ToString(Date datetime) { // TODO - Cambio en el tipo de formato de retorno
		try {
			return sdfDatetime24.format(datetime);
		} catch (Exception ex) {
			return null;
		}
	}
	
	
	/**
	 * Obtiene el calendario en formato UTC a partir de un objeto Date
	 * 
	 * @param Date con la fecha a convertir
	 * @return Calendar
	 */
	public static Calendar getUtcCalendarFromDate(Date date) { // TODO - modificacion menor
	    Calendar calendar = Calendar.getInstance(UTC_TIME_ZONE);
        calendar.setTime(date);
        return calendar;
	}
	
	/**
	 * Obtiene un nuevo objeto Calendario [En formato UTC]
	 * 
	 * @return Calendar
	 */
	public static Calendar getNewUtcCalendar() { // TODO Modificacion menor
        return getUtcCalendarFromDate(new Date());
	}
	
	
	/**
	 * Convierte una Fecha a una nueva fecha aplicando un TimeZone
	 * 
	 * @param Date a convertir
	 * @param timeZone 
	 * @return Objeto Date con timeZone aplicado
	 */ 
	public static Date applyTimezoneToDate(Date date, String timeZone) {
	    Date response = null;
	    SimpleDateFormat dateFormatBack = new SimpleDateFormat(sdfUTCFormat);
        dateFormatBack.setTimeZone(TimeZone.getTimeZone(timeZone));
        try {
            response = dateFormatBack.parse(dateFormatBack.format(date));
        } catch (ParseException e) {
            return null;
        }
        return response;
	}
	
	/**
	 * Convierte una Fecha a una nueva fecha aplicando un TimeZone
	 * 
	 * @param Date a convertir
	 * @param timeZone 
	 * @return Objeto Date con timeZone aplicado
	 */
	public static Date applyTimezone(Date date, String timeZone) {
		Date response = null;
		try {
			TimeZone tz = TimeZone.getTimeZone(timeZone);
			FastDateFormat dateFormatBack = FastDateFormat.getInstance(sdfUTCFormat, tz);
			response = dateFormatBack.parse(dateFormatBack.format(date.getTime()));
		} catch (Exception e) {
			LOGGER.error("Ocurrio un error en el metodo applyTimezone");
		}
		return response;
    }
	
	/**
	 * Convierte un objeto String a uno del tipo Date de java.util.date
	 * con zona horaria
	 * 
	 * @param String en formato "yyyy-MM-dd'T'hh:mm:ss"
	 * @return java.util.date
	 **/
	public static Date stringToTimeZoned(String string) {
		try {
			return sdfDateTimeZoned.parse(string);
	} catch (Exception ex) {
			return null;
		}
	}

	/** 
	 * Convierte un objeto de tipo Date a XMLGregorianCalendar en UTC
	 * 
	 * @param Objeto ZonedDateTime
	 * @return XMLGregorianCalendar
	 */
	public static XMLGregorianCalendar dateToXmlGregorianCalendar(ZonedDateTime zonedDateTime) {
		XMLGregorianCalendar xmlGregorianCalendar = null;
		if(!ValidatorUtil.isNull(zonedDateTime)) {
			try {
				xmlGregorianCalendar = DatatypeFactory.newInstance().newXMLGregorianCalendar(GregorianCalendar.from(zonedDateTime));
				xmlGregorianCalendar.setMillisecond(DatatypeConstants.FIELD_UNDEFINED);
				xmlGregorianCalendar.setTimezone(DatatypeConstants.FIELD_UNDEFINED);
			} catch (Exception e) {
				LOGGER.error("Ocurrio un error al transformar un Date a XMLGregorianCalendar en UTC");
			}
		}
	    return xmlGregorianCalendar;
	}
	
	/**
	 * Convierte un objeto tipo Date a un String con formato folio
	 *
	 * @param Objeto Date a convertir
	 * @return String con formato "yyyyMMdd"
	 */
	public static String dateToStringFolioFormat(Date date) {
		try {
			return sdfFolio.format(date);
		} catch (Exception e) {
			return null;
		}
	}
	
	/**
	 * Convierte un String a un objeto Date con formato para factura
	 *
	 * @param Objeto Date a convertir
	 * @return String con formato "yyyy-MM-dd'T'HH:mm:ss"
	 */
	public static Date stringToDateFactura(String datetime) {
		try {
			return sdfFactura.parse(datetime);
		} catch (Exception ex) {
			return null;
		}
	}

	/**
	 * Convierte un objeto Date a uno del tipo String en formato "yyyy-MM-dd'T'HH:mm:ss"
	 * 
	 * @param Date con la fecha a convertir
	 * @return String formato "yyyy-MM-dd'T'HH:mm:ss"
	 **/
	public static String datetimeToStringZoned(Date datetime) {
		try {
			return sdfDateTimeZoned.format(datetime); 
		} catch (Exception ex) {
			return null;
		}
	}
	
	/**
	 * Convierte un objeto Date a un String con formato para notificaciones
	 *
	 * @param Objeto Date a convertir
	 * @return String con el formato para notificaciones SMS
	 */
	public static String diaLetraToStringSms(Date date) {
		try {
			return sdfDiaLetraSmsNotificacion.format(date);
		} catch (Exception e) {
			return null;
		}
	}
	
	/**
	 * Convierte una objeto Date a un String que indica el dia numerico
	 *
	 * @param Objeto Date a convertir
	 * @return String con el formato de dia numerico
	 */
	public static String diaNumericoToStringSms(Date date) {
		try {
			return sdfDiaNumericoSmsNotificacion.format(date);
		} catch (Exception e) {
			return null;
		}
	}
	
	/**
	 * Convierte un objeto Date a un String que indica el mes numerico
	 *
	 * @param Objeto Date a convertir
	 * @return String con el formato de mes numerico
	 */
	public static String mesToStringSms(Date date) {
		try {
			return sdfMesSmsNotificacion.format(date);
		} catch (Exception e) {
			return null;
		}
	}
	
	/**
	 * Convierte un objeto Date a un String que indica el numero del anio
	 *
	 * @param Objeto Date a convertir
	 * @return String con el formato del numero de año
	 */
	public static String anioToStringSms(Date date) {
		try {
			return sdfAnioSmsNotificacion.format(date);
		} catch (Exception e) {
			return null;
		}
	}
	
	/**
	 * Obtiene el numero de dias entre dos fechas
	 * @param date1 Fecha inicial del calculo
	 * @param date2 Fecha final del calculo
	 * @return Numero de dias entre date1 y date2
	 */
	public static Integer getDaysBetween(Date date1, Date date2) {
		
		if(ValidatorUtil.isNull(date1) || ValidatorUtil.isNull(date2)) {
			return null;
		}
		LocalDate localDate1 = date1.toInstant().atZone(ZoneId.systemDefault()).toLocalDate();
	    LocalDate localDate2 = date2.toInstant().atZone(ZoneId.systemDefault()).toLocalDate();
	 
	    return (int)ChronoUnit.DAYS.between(localDate1, localDate2);
	}
	
	/* Ejemplo("fecha", "utc",Locale.ENGLISH) */
    public static String dateToStringWithFormat(Date date, String timeZone, Locale locale) {
        String response = null;
        if(!ValidatorUtil.isNull(date)) {
            FastDateFormat fastDateFormat = FastDateFormat.getInstance(GeneralConstants.DATE_TIME_FORMAT_YYYY_MM_DD, TimeZone.getTimeZone(timeZone), locale);
    		response = fastDateFormat.format(date);
        }
		return response;
	}
	
	/**
	 * Convierte un objeto tipo Xml gregorian calendar a un String.
	 *
	 * @param xmlGregorianCalendar the xml gregorian calendar
	 * @param timeZone the time zone
	 * @return the string
	 */
	public static String xmlGregorianCalendarToString(XMLGregorianCalendar xmlGregorianCalendar, String timeZone) {
		String dateString = null;
		Calendar calendar = xmlGregorianCalendar.toGregorianCalendar();
		sdfDate.setTimeZone(TimeZone.getTimeZone(timeZone));
		try {
			dateString = sdfDate.format(calendar.getTime());
		} catch (Exception e) {
			LOGGER.error("Ocurrio un al convertir un XMLGregorianCalendar a string", e);
		}

		return dateString;
	}
	
	/**
	 * Convierte una Fecha (objeto tipo Date) a un String con Timezon
	 * Este metodo ayuda a trabajar con diferentes zonas ya que Date, no soporta TimeZones 
	 *
	 * @param date
	 * @param timeZone
	 * @return the string
	 */
	public static String dateToStringWithTimeZone(Date date, String timeZone) {
	    sdfMobile.setTimeZone(TimeZone.getTimeZone(timeZone));
        return sdfMobile.format(date);
	}
	
	/**
	 * Convierte un String con TimeZone a un objeto Date 
	 * 
	 * @param datetime
	 * @return
	 */
	public static Date stringToDateWithTimeZone(String datetime, String timeZone) {
		try {
			if(ValidatorUtil.isNullOrEmpty(timeZone)) {
				sdfRequestDate.setTimeZone(TimeZone.getDefault());
			}else {
				sdfRequestDate.setTimeZone(TimeZone.getTimeZone(timeZone));				
			}
			return sdfRequestDate.parse(datetime);
		} catch (Exception ex) {
			return null;
		}
	}
	
	/**
	 * Force time of specific TimeZone
	 *
	 * @param date
	 * @param originalTimeZone
	 * @param desiredTimeZone
	 * @return the string
	 */
	public static Date forceTimeZone(Date date, String originalTimeZone, String desiredTimeZone) {
		String stringDate = date.toString();
		Date response = null;
		stringDate = stringDate.replaceAll(originalTimeZone, desiredTimeZone);
		DateFormat format = new SimpleDateFormat("EEE MMM dd HH:mm:ss zzz yyyy", Locale.ENGLISH);
		try {
			response = format.parse(stringDate);
		} catch (ParseException e) {
			LOGGER.error("Ocurrio un al forzar el TimeZone", e);
		}
		return response;
	}
	
	/**
     * Obtiene la fecha a partir de un token
     *
     * @param date
     * @return the date
     */
    public static Date getDateFromToken(String date) {
        Date response = null;
        DateFormat format = new SimpleDateFormat("EEE MMM dd HH:mm:ss zzz yyyy", Locale.ENGLISH);
        try {
            response = format.parse(date);
        } catch (ParseException e) {
            LOGGER.error("Ocurrio un al obtener la fecha del token", e);
        }
        return response;
    }
    
	/**
	 * Convierte un objeto tipo Date a un String con TimeZone
	 * 
	 * @param date
	 * @return
	 */
	public static String requestDateToStringWithTimeZone(Date date, String timeZone) {
		try {
			if(ValidatorUtil.isNullOrEmpty(timeZone)) {
				sdfRequestDate.setTimeZone(TimeZone.getDefault());
			}else {
				sdfRequestDate.setTimeZone(TimeZone.getTimeZone(timeZone));				
			}
			return sdfRequestDate.format(date);
		} catch (Exception ex) {
			return null;
		}
	}
	
	
	/**
	 * Convierte un objeto Date (SQL) a un objeto tipo Date (Util)
	 * 
	 * @param sqlDate
	 * @return
	 */
	public static Date convertFromSqlDateToUtilDate(
            java.sql.Date sqlDate) {
        Date utilDate = null;
        if (sqlDate != null) {
            utilDate = new Date(sqlDate.getTime());
        }
        return utilDate;
    }
	
	/**
	 * Convierte un objeto timestamp (SQL) a un objeto Date (Util)
	 * @param timestampDate
	 * @return
	 */
	public static Date convertFromSqlTimestampToUtilDate(
            java.sql.Timestamp timestampDate) {
        Date utilDate = null;
        if (timestampDate != null) {
            utilDate = new Date(timestampDate.getTime());
        }
        return utilDate;
    }
	
	/**
	 * Convierte una cadena a un objeto de tipo fecha
	 * @param strDate 		Cadena que se desea convertir en date
	 * @param formatDate 	Cadena con el formato de fecha que se desea convertir
	 * @return 				Regresa un objeto de tipo Date con el formato indicado
	 */
	public static Date transformStringToDate(String strDate, String formatDate) {
		Date date = null;
		if (!ValidatorUtil.isNullOrEmpty(strDate)) {
			SimpleDateFormat formato = new SimpleDateFormat(formatDate);
			try {
				date = formato.parse(strDate);
			} catch (ParseException e) {
				date = null;
			}
		}
		return date;
	}
	
	
	/**
	 * Convierte un objeto de tipo date a una cadena con el formato indicado
	 * @param date			Fecha que se desea convertir a cadena
	 * @param formatDate	Cadena con el formato de fecha que se desea obtener
	 * @return 				Regresa una cadena con la fecha en el formato indicado
	 */
	public static String transformDateToString(Date date, String formatDate) {
		String strDate = null;
		if (!ValidatorUtil.isNull(date)) {
			SimpleDateFormat formato = new SimpleDateFormat(formatDate);
			try {
				strDate = formato.format(date);
				
			}catch (Exception e) {
				strDate = null;
			}
		}
		return strDate;
	}
	
	/**
	 * Convierte un objeto String en formato "yyyy-MM-dd'T'HH:mm" a uno del tipo Date
	 * 
	 * @param string formato "yyyy-MM-dd'T'HH:mm"
	 * @return Date con la fecha a convertir
	 **/
	public static Date stringToDatetimeT24(String datetime) {
		try {
			return sdfDatetimeT24H.parse(datetime);
		} catch (Exception ex) {
			return null;
		}
	}
	
	/**
	 * Convierte un objeto Date a un String con formato (dd de MMMM de yyyy) para las apps
	 *
	 * @param date
	 * @return the string
	 */
	public static String dateToStringForApp(Date date) {
        return sdfMobileFormat.format(date);
	}
	
	/**
	 * Convierte un objeto Date a un String con formato (dd/mm/yyyy) para las apps
	 *
	 * @param date
	 * @return the string
	 */
	public static String dateToStringSeparateDiagonal(Date date) { // TODO - Correccion de javadoc
		String rValue = null;
		try {
			rValue = sdfSeparateDiagonal.format(date);
		} catch (Exception ex) {
			rValue = null;
		}
		return rValue;
	}
}